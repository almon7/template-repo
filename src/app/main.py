from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from app.log import configure_logging
from app.settings import settings


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
    return _app


app = create_app()
