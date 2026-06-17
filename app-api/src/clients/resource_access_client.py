from typing import Any

import httpx

from src.core.settings import settings


class ResourceAccessClient:
    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = base_url or settings.resource_api_base_url

    async def get(self, path: str, headers: dict[str, str] | None = None) -> Any:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=10.0) as client:
            response = await client.get(path, headers=headers)
            response.raise_for_status()
            return response.json() if response.content else None

    async def post(
        self, path: str, payload: dict[str, Any], headers: dict[str, str] | None = None
    ) -> Any:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=10.0) as client:
            response = await client.post(path, json=payload, headers=headers)
            response.raise_for_status()
            return response.json() if response.content else None

    async def put(
        self, path: str, payload: dict[str, Any], headers: dict[str, str] | None = None
    ) -> Any:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=10.0) as client:
            response = await client.put(path, json=payload, headers=headers)
            response.raise_for_status()
            return response.json() if response.content else None

    async def delete(self, path: str, headers: dict[str, str] | None = None) -> Any:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=10.0) as client:
            response = await client.delete(path, headers=headers)
            response.raise_for_status()
            return response.json() if response.content else None
