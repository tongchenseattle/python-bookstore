from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "app-api"
    app_env: str = Field(default="development", alias="APP_ENV")
    app_api_log_level: str = Field(default="INFO", alias="APP_API_LOG_LEVEL")
    resource_api_base_url: str = Field(
        default="http://localhost:8001", alias="RESOURCE_API_BASE_URL"
    )
    correlation_header_name: str = Field(
        default="X-Correlation-ID", alias="CORRELATION_HEADER_NAME"
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
