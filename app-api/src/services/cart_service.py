from src.clients.resource_access_client import ResourceAccessClient


class CartService:
    def __init__(self, client: ResourceAccessClient | None = None) -> None:
        self.client = client or ResourceAccessClient()

    async def add_item(self, payload: dict):
        return await self.client.post("/internal/storefront/orders/cart-items", payload)

    async def ensure_cart(self, cart_id: str, session_id: str):
        return await self.client.post(
            f"/internal/storefront/orders/carts/{cart_id}/ensure",
            {"session_id": session_id},
        )

    async def get_cart(self, cart_id: str):
        return await self.client.get(f"/internal/storefront/orders/carts/{cart_id}")

    async def set_item_quantity(self, cart_id: str, book_id: str, quantity: int):
        return await self.client.put(
            f"/internal/storefront/orders/carts/{cart_id}/items/{book_id}",
            {"quantity": quantity},
        )

    async def remove_item(self, cart_id: str, book_id: str):
        return await self.client.delete(
            f"/internal/storefront/orders/carts/{cart_id}/items/{book_id}"
        )
