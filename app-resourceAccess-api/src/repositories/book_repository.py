import uuid

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

    def get_published_by_id(self, book_id: str) -> Book | None:
        try:
            parsed_id = uuid.UUID(book_id)
        except ValueError:
            return None

        stmt = select(Book).where(Book.id == parsed_id, Book.status == "published")
        return self.db.scalar(stmt)
