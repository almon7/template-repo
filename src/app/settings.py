from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "template-app"

    # deployment context: development (default), testing (skip slow startup tasks like DB migrations in CI/pytest), or production.
    # In production, Swagger UI is disabled and debug log levels are forbidden.
    environment: Literal["development", "testing", "production"] = "production"

    # Single source of truth for verbosity: set LOG_LEVEL=DEBUG or TRACE to enable debug mode; both are blocked in production.
    log_level: Literal["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"] = "INFO"


settings = Settings()
