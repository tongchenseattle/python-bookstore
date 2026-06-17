from src.clients.resource_access_client import ResourceAccessClient


class CartService:
    def __init__(self, client: ResourceAccessClient | None = None) -> None:
        self.client = client or ResourceAccessClient()

    async def add_item(self, payload: dict):
        return await self.client.post("/internal/orders/cart-items", payload)
