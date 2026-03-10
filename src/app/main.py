from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.log import configure_logging
from app.routers import health
from app.settings import settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Attach security-hardening response headers to every reply."""

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        return response


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None]:
    """Configure logging and emit startup/shutdown lifecycle events."""
    configure_logging()
    logger.info("Starting {name} [{env}]", name=settings.app_name, env=settings.environment)
    yield
    logger.info("Shutting down {name}", name=settings.app_name)


def create_app() -> FastAPI:
    """Application factory — keeps instantiation testable and explicit."""
    _app = FastAPI(
        title=settings.app_name,
        lifespan=lifespan,
        # When True, FastAPI includes full Python tracebacks in 500 error
        # responses. Useful locally; blocked in production by the settings
        # validator so this can never be True there.
        debug=settings.debug,
        # Disable interactive docs in production to reduce attack surface.
        docs_url="/docs" if settings.environment != "production" else None,
        redoc_url="/redoc" if settings.environment != "production" else None,
        openapi_url="/openapi.json" if settings.environment != "production" else None,
    )

    # Security headers on every response
    _app.add_middleware(SecurityHeadersMiddleware)

    # Guard against HTTP Host header attacks
    if settings.environment == "production":
        _app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

    _app.include_router(health.router)

    return _app


app = create_app()
