from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.catalog import Book


class BookRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_published(self, category_id: str | None = None) -> list[Book]:
        stmt = select(Book).where(Book.status == "published")
        if category_id:
            stmt = stmt.where(Book.category_id == category_id)
        return list(self.db.scalars(stmt))
