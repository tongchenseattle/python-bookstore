from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class BookSummary(BaseModel):
    id: UUID
    title: str
    publish_date: date
    price: Decimal
    category_id: UUID


class CartItemPayload(BaseModel):
    book_id: UUID
    quantity: int = Field(ge=1)


class CheckoutSubmitPayload(BaseModel):
    cart_id: UUID
