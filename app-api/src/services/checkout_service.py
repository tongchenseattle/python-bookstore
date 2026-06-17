import logging

from fastapi import HTTPException, status

from src.clients.resource_access_client import ResourceAccessClient

logger = logging.getLogger(__name__)


class CheckoutService:
    def __init__(self, client: ResourceAccessClient | None = None) -> None:
        self.client = client or ResourceAccessClient()

    async def submit(self, user: dict | None, payload: dict):
        if not user:
            logger.warning("checkout_denied_unauthenticated", extra={"event": "checkout_denied"})
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

        request_payload = {
            "user_id": user.get("id") or payload.get("user_id"),
            "cart_id": payload["cart_id"],
            "total_amount": payload.get("total_amount", 0),
        }
        result = await self.client.post("/internal/orders", request_payload)
        logger.info("checkout_submitted", extra={"event": "checkout_success"})
        return result
