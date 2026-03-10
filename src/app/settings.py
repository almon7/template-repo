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

    # deployment context: development (default), testing (skip slow startup tasks like DB migrations in CI/pytest),
    # or production. In production, Swagger UI is disabled and debug log levels are forbidden.
    environment: Literal["development", "testing", "production"] = "development"

    # Single source of truth for verbosity level: set to DEBUG/TRACE to enable debug mode;
    # Both DEBUG and TRACE logging levels are blocked in production.
    log_level: Literal["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    # Allowed HTTP Host header values, consumed by TrustedHostMiddleware.
    # Defaults to ["*"] (allow any host) so the template works out of the box.
    # In production you MUST restrict this to your actual domain(s):
    #   ALLOWED_HOSTS=["api.example.com", "www.example.com"]
    # The production validator below will reject the wildcard to enforce this.
    allowed_hosts: list[str] = ["*"]

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
        """Prevent insecure settings in production."""
        if self.environment == "production":
            if self.log_level in _DEBUG_LEVELS:
                msg = (
                    f"log_level={self.log_level!r} is not permitted when ENVIRONMENT=production. "
                    "Use INFO, WARNING, ERROR, or CRITICAL."
                )
                raise ValueError(msg)
            if self.allowed_hosts == ["*"]:
                msg = (
                    "allowed_hosts=['*'] is not permitted when ENVIRONMENT=production. "
                    "Set ALLOWED_HOSTS to your actual domain(s), e.g. ['api.example.com']."
                )
                raise ValueError(msg)
        return self


settings = Settings()
