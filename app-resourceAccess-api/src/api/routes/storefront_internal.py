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
    item = CartItem(
        id=uuid.uuid4(),
        cart_id=uuid.UUID(payload["cart_id"]),
        book_id=uuid.UUID(payload["book_id"]),
        quantity=int(payload["quantity"]),
        unit_price=float(payload.get("unit_price", 0)),
        line_total=float(payload.get("line_total", 0)),
    )
    created = repo.add_cart_item(item.cart_id, item)
    db.commit()
    return {"id": str(created.id)}


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
