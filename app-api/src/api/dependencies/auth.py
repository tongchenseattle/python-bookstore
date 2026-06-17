from fastapi import HTTPException, Request, status


async def require_authenticated_user(request: Request) -> dict:
    user = request.session.get("user") if hasattr(request, "session") else None
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    return user
