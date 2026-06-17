from fastapi import APIRouter, Depends, Request

from src.api.dependencies.auth import require_authenticated_user
from src.schemas.storefront import CartItemPayload, CheckoutSubmitPayload
from src.services.cart_service import CartService
from src.services.catalog_service import CatalogService
from src.services.checkout_service import CheckoutService

router = APIRouter(tags=["storefront"])


def get_catalog_service() -> CatalogService:
    return CatalogService()


def get_cart_service() -> CartService:
    return CartService()


def get_checkout_service() -> CheckoutService:
    return CheckoutService()


@router.get("/catalog/categories")
async def get_categories(service: CatalogService = Depends(get_catalog_service)):
    return await service.list_categories()


@router.get("/catalog/books")
async def get_books(
    categoryId: str | None = None,
    service: CatalogService = Depends(get_catalog_service),
):
    return await service.list_books(categoryId)


@router.get("/catalog/books/{bookId}")
async def get_book_detail(
    bookId: str,
    service: CatalogService = Depends(get_catalog_service),
):
    return await service.get_book(bookId)


@router.post("/cart/items")
async def add_cart_item(payload: CartItemPayload, service: CartService = Depends(get_cart_service)):
    return await service.add_item(payload.model_dump())


@router.post("/checkout/submit")
async def submit_checkout(
    payload: CheckoutSubmitPayload,
    request: Request,
    user: dict = Depends(require_authenticated_user),
    service: CheckoutService = Depends(get_checkout_service),
):
    return await service.submit(user, payload.model_dump())
