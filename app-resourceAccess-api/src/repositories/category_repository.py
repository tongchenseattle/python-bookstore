from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.catalog import Category


class CategoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_active(self) -> list[Category]:
        stmt = select(Category).where(Category.status == "active")
        return list(self.db.scalars(stmt))
