from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.user_account import UserAccount


class AuthRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_user_by_email(self, email: str) -> UserAccount | None:
        stmt = select(UserAccount).where(UserAccount.email == email, UserAccount.is_active)
        return self.db.scalar(stmt)
