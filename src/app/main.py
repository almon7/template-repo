import uuid
from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.log import configure_logging
from app.routers import health
from app.settings import settings

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Attach security-hardening response headers to every reply."""

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        # X-XSS-Protection is deprecated (removed in Chrome ≥78, never in Firefox);
        # Content-Security-Policy is the modern, effective replacement.
        response.headers["Content-Security-Policy"] = "default-src 'none'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        return response


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Propagate or generate a request-scoped correlation ID.

    * Reads ``X-Request-ID`` from the incoming request (useful when a gateway
      or client already stamps the request).
    * Falls back to a freshly generated UUID v4 when the header is absent.
    * Binds the ID to the loguru context so every log record emitted during
      that request automatically includes ``request_id``.
    * Returns the ID in the ``X-Request-ID`` response header so clients and
      load balancers can correlate their logs with ours.
    """

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        with logger.contextualize(request_id=request_id):
            response: Response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None]:
    """Configure logging and emit startup/shutdown lifecycle events."""
    configure_logging()
    logger.info("Starting {name} [{env}]", name=settings.app_name, env=settings.environment)
    yield
    logger.info("Shutting down {name}", name=settings.app_name)


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------


def create_app() -> FastAPI:
    """Application factory — keeps instantiation testable and explicit."""
    _app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
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

    # Middleware is applied in reverse registration order: the last
    # add_middleware() call becomes the outermost wrapper, so it executes
    # first on every request.  The intended request order is:
    #   TrustedHostMiddleware → RequestIDMiddleware → SecurityHeadersMiddleware → route
    _app.add_middleware(SecurityHeadersMiddleware)
    _app.add_middleware(RequestIDMiddleware)

    # Guard against HTTP Host header attacks.
    # allowed_hosts defaults to ["*"] in development; the settings validator
    # rejects ["*"] in production, ensuring real domain(s) are always set.
    _app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)

    # CORS — only enabled when cors_origins is non-empty.
    # Set CORS_ORIGINS=["https://app.example.com"] to allow a browser frontend.
    if settings.cors_origins:
        _app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    _app.include_router(health.router)

    return _app


app = create_app()
