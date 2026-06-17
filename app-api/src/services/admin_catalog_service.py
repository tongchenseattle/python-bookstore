from src.clients.resource_access_client import ResourceAccessClient


class AdminCatalogService:
    def __init__(self, client: ResourceAccessClient | None = None) -> None:
        self.client = client or ResourceAccessClient()

    async def create_category(self, payload: dict):
        return await self.client.post("/internal/admin/categories", payload)

    async def create_book(self, payload: dict):
        if "price" in payload:
            payload["price"] = round(float(payload["price"]), 2)
        return await self.client.post("/internal/admin/books", payload)
