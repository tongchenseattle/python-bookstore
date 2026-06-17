from fastapi import Depends, HTTPException, status

from src.api.dependencies.auth import require_authenticated_user


async def require_admin_user(user: dict = Depends(require_authenticated_user)) -> dict:
    if user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required")
    return user
