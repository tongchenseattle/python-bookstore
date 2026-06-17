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
    cart_id: UUID
    book_id: UUID
    quantity: int = Field(ge=1)


class CartEnsurePayload(BaseModel):
    session_id: str = Field(min_length=1, max_length=128)


class CartItemQuantityPayload(BaseModel):
    quantity: int = Field(ge=1)


class CheckoutSubmitPayload(BaseModel):
    cart_id: UUID
