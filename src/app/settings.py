from typing import Literal

from pydantic import computed_field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Log levels considered 'debug mode' - they expose internal details and must not be used in production.
_DEBUG_LEVELS = frozenset({"TRACE", "DEBUG"})

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

    @computed_field  # type: ignore[prop-decorator]
    @property
    def debug(self) -> bool:
        """
        True when log_level is TRACE or DEBUG.
        Passed to FastAPI(debug=...) to include Python tracebacks in 500 error responses — not a separate env var.
        """
        return self.log_level in _DEBUG_LEVELS

    @model_validator(mode="after")
    def validate_production_constraints(self) -> "Settings":
        """Prevent debug log levels in production."""
        if self.environment == "production" and self.log_level in _DEBUG_LEVELS:
            msg = (
                f"log_level={self.log_level!r} is not permitted when ENVIRONMENT=production. "
                "Use INFO, WARNING, ERROR, or CRITICAL."
            )
            raise ValueError(msg)
        return self


settings = Settings()
