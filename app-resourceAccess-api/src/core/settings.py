from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "app-resourceAccess-api"
    app_env: str = Field(default="development", alias="APP_ENV")
    app_log_level: str = Field(default="INFO", alias="RESOURCE_API_LOG_LEVEL")
    sqlserver_connection_string: str = Field(
        default=(
            "mssql+pyodbc:///?odbc_connect="
            "Driver%3D%7BODBC+Driver+17+for+SQL+Server%7D%3B"
            "Server%3D%28localdb%29%5CMSSQLLocalDB%3B"
            "Database%3Dbookstore_local%3B"
            "Trusted_Connection%3Dyes%3B"
            "TrustServerCertificate%3Dyes%3B"
        ),
        alias="SQLSERVER_CONNECTION_STRING",
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
