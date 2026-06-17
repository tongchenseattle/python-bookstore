import datetime as dt
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.models.order import CartItem, PseudoOrder
from src.repositories.book_repository import BookRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.order_repository import OrderRepository

router = APIRouter(prefix="/internal/storefront", tags=["storefront-internal"])


@router.get("/categories")
async def list_categories(db: Session = Depends(get_db)):
    repo = CategoryRepository(db)
    return repo.list_active()


@router.get("/books")
async def list_books(category_id: str | None = Query(default=None), db: Session = Depends(get_db)):
    repo = BookRepository(db)
    return repo.list_published(category_id)


@router.get("/books/{book_id}")
async def get_book(book_id: str, db: Session = Depends(get_db)):
    repo = BookRepository(db)
    book = repo.get_published_by_id(book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.post("/orders/cart-items")
async def add_cart_item(payload: dict, db: Session = Depends(get_db)):
    repo = OrderRepository(db)
    created = repo.add_cart_item(
        cart_id=uuid.UUID(payload["cart_id"]),
        book_id=uuid.UUID(payload["book_id"]),
        quantity=int(payload["quantity"]),
    )
    db.commit()
    return {"id": str(created.id)}


@router.post("/orders/carts/{cart_id}/ensure")
async def ensure_cart(cart_id: str, payload: dict, db: Session = Depends(get_db)):
    repo = OrderRepository(db)
    cart = repo.ensure_cart(uuid.UUID(cart_id), payload.get("session_id", "browser-session"))
    db.commit()
    return {"cart_id": str(cart.id), "status": cart.status}


@router.get("/orders/carts/{cart_id}")
async def get_cart(cart_id: str, db: Session = Depends(get_db)):
    repo = OrderRepository(db)
    return repo.get_cart_view(uuid.UUID(cart_id))


@router.put("/orders/carts/{cart_id}/items/{book_id}")
async def set_cart_item_quantity(cart_id: str, book_id: str, payload: dict, db: Session = Depends(get_db)):
    repo = OrderRepository(db)
    item = repo.set_item_quantity(
        cart_id=uuid.UUID(cart_id),
        book_id=uuid.UUID(book_id),
        quantity=int(payload["quantity"]),
    )
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    db.commit()
    return {"book_id": str(item.book_id), "quantity": int(item.quantity)}


@router.delete("/orders/carts/{cart_id}/items/{book_id}")
async def remove_cart_item(cart_id: str, book_id: str, db: Session = Depends(get_db)):
    repo = OrderRepository(db)
    removed = repo.remove_item(cart_id=uuid.UUID(cart_id), book_id=uuid.UUID(book_id))
    if not removed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    db.commit()
    return {"removed": True}


@router.post("/orders")
async def create_order(payload: dict, db: Session = Depends(get_db)):
    repo = OrderRepository(db)
    order = PseudoOrder(
        id=uuid.uuid4(),
        order_number=f"PO-{uuid.uuid4().hex[:10]}",
        user_id=uuid.UUID(payload["user_id"]),
        cart_id=uuid.UUID(payload["cart_id"]),
        total_amount=float(payload.get("total_amount", 0)),
        status="confirmed",
        confirmed_at=dt.datetime.utcnow(),
    )
    created = repo.create_pseudo_order(order)
    db.commit()
    return {"id": str(created.id), "order_number": created.order_number}
