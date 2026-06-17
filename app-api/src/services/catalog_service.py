from src.clients.resource_access_client import ResourceAccessClient


class CatalogService:
    def __init__(self, client: ResourceAccessClient | None = None) -> None:
        self.client = client or ResourceAccessClient()

    async def list_categories(self):
        return await self.client.get("/internal/storefront/categories")

    async def list_books(self, category_id: str | None = None):
        path = "/internal/storefront/books"
        if category_id:
            path += f"?category_id={category_id}"
        return await self.client.get(path)
