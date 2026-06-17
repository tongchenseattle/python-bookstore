from fastapi import APIRouter, Depends

from src.api.dependencies.admin_auth import require_admin_user
from src.schemas.admin import BookCreatePayload, CategoryCreatePayload
from src.services.admin_catalog_service import AdminCatalogService

router = APIRouter(prefix="/admin", tags=["admin"])


def get_admin_catalog_service() -> AdminCatalogService:
    return AdminCatalogService()


@router.post("/categories")
async def create_category(
    payload: CategoryCreatePayload,
    _user: dict = Depends(require_admin_user),
    service: AdminCatalogService = Depends(get_admin_catalog_service),
):
    return await service.create_category(payload.model_dump())


@router.post("/books")
async def create_book(
    payload: BookCreatePayload,
    _user: dict = Depends(require_admin_user),
    service: AdminCatalogService = Depends(get_admin_catalog_service),
):
    return await service.create_book(payload.model_dump())
