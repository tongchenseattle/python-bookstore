import uuid
from decimal import Decimal
import datetime as dt

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.catalog import Book
from src.models.order import Cart, CartItem, PseudoOrder


class OrderRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _recalculate_cart_subtotal(self, cart_id: uuid.UUID) -> None:
        cart = self.db.get(Cart, cart_id)
        if not cart:
            return

        items = list(self.db.scalars(select(CartItem).where(CartItem.cart_id == cart_id)))
        subtotal = sum(float(item.line_total) for item in items)
        cart.subtotal = subtotal
        cart.updated_at = dt.datetime.utcnow()

    def ensure_cart(self, cart_id: uuid.UUID, session_id: str) -> Cart:
        cart = self.db.get(Cart, cart_id)
        if cart:
            return cart

        cart = Cart(
            id=cart_id,
            user_id=None,
            session_id=session_id,
            status="active",
            subtotal=0,
            created_at=dt.datetime.utcnow(),
            updated_at=dt.datetime.utcnow(),
        )
        self.db.add(cart)
        self.db.flush()
        return cart

    def add_cart_item(self, cart_id: uuid.UUID, book_id: uuid.UUID, quantity: int) -> CartItem:
        self.ensure_cart(cart_id, session_id="browser-session")

        book = self.db.get(Book, book_id)
        if not book:
            raise ValueError("Book not found")

        existing = self.db.scalar(
            select(CartItem).where(CartItem.cart_id == cart_id, CartItem.book_id == book_id)
        )

        unit_price = float(book.price)
        if existing:
            existing.quantity += quantity
            existing.unit_price = unit_price
            existing.line_total = float(Decimal(existing.quantity) * Decimal(str(unit_price)))
            item = existing
        else:
            item = CartItem(
                id=uuid.uuid4(),
                cart_id=cart_id,
                book_id=book_id,
                quantity=quantity,
                unit_price=unit_price,
                line_total=float(Decimal(quantity) * Decimal(str(unit_price))),
            )
            self.db.add(item)

        self.db.flush()
        self._recalculate_cart_subtotal(cart_id)
        self.db.flush()
        return item

    def set_item_quantity(self, cart_id: uuid.UUID, book_id: uuid.UUID, quantity: int) -> CartItem | None:
        item = self.db.scalar(
            select(CartItem).where(CartItem.cart_id == cart_id, CartItem.book_id == book_id)
        )
        if not item:
            return None

        item.quantity = quantity
        item.line_total = float(Decimal(quantity) * Decimal(str(float(item.unit_price))))
        self.db.flush()
        self._recalculate_cart_subtotal(cart_id)
        self.db.flush()
        return item

    def remove_item(self, cart_id: uuid.UUID, book_id: uuid.UUID) -> bool:
        item = self.db.scalar(
            select(CartItem).where(CartItem.cart_id == cart_id, CartItem.book_id == book_id)
        )
        if not item:
            return False

        self.db.delete(item)
        self.db.flush()
        self._recalculate_cart_subtotal(cart_id)
        self.db.flush()
        return True

    def get_cart_view(self, cart_id: uuid.UUID) -> dict:
        cart = self.db.get(Cart, cart_id)
        if not cart:
            return {"cart_id": str(cart_id), "items": [], "subtotal": 0.0}

        stmt = (
            select(CartItem, Book)
            .join(Book, CartItem.book_id == Book.id)
            .where(CartItem.cart_id == cart_id)
        )
        rows = self.db.execute(stmt).all()

        items = []
        for cart_item, book in rows:
            items.append(
                {
                    "book_id": str(cart_item.book_id),
                    "title": book.title,
                    "price": float(cart_item.unit_price),
                    "quantity": int(cart_item.quantity),
                    "line_total": float(cart_item.line_total),
                }
            )

        return {
            "cart_id": str(cart.id),
            "status": cart.status,
            "items": items,
            "subtotal": float(cart.subtotal),
        }

    def create_pseudo_order(self, order: PseudoOrder) -> PseudoOrder:
        self.db.add(order)
        self.db.flush()
        return order

    def get_cart(self, cart_id: uuid.UUID) -> Cart | None:
        return self.db.get(Cart, cart_id)
