from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse

from src.api.routes.admin import router as admin_router
from src.api.routes.health import router as health_router
from src.api.routes.storefront import router as storefront_router
from src.core.settings import settings

app = FastAPI(title=settings.app_name)
app.include_router(storefront_router)
app.include_router(admin_router)
app.include_router(health_router)


@app.get("/swagger", include_in_schema=False)
async def swagger_ui():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url or "/openapi.json",
        title=f"{settings.app_name} - Swagger UI",
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"error": "internal_server_error", "detail": str(exc)},
    )
