from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session

from src.core.database import get_db

router = APIRouter(prefix="/internal/admin", tags=["admin-internal"])


@router.post("/categories")
async def create_category(payload: dict, _db: Session = Depends(get_db)):
    return {"status": "created", "payload": payload}


@router.delete("/categories/{category_id}")
async def delete_category(category_id: str, _db: Session = Depends(get_db)):
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Category {category_id} has linked books",
    )


@router.post("/books")
async def create_book(payload: dict, _db: Session = Depends(get_db)):
    return {"status": "created", "payload": payload}


@router.patch("/books/{book_id}")
async def update_book(
    book_id: str,
    payload: dict,
    if_match: str | None = Header(default=None, alias="If-Match"),
    _db: Session = Depends(get_db),
):
    if if_match is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Missing If-Match concurrency token",
        )
    return {"status": "updated", "book_id": book_id, "payload": payload}
