from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class CategoryCreatePayload(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=1000)


class BookCreatePayload(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    publish_date: date
    price: Decimal = Field(ge=0)
    description: str | None = Field(default=None, max_length=4000)
    category_id: UUID
    status: str
