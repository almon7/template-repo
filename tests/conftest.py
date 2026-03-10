"""
Shared pytest fixtures and configuration.
Add fixtures here that are needed across multiple test modules.
"""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from loguru import logger

from app.main import app


@pytest.fixture(autouse=True)
def silence_logs() -> Generator[None]:
    """Remove all loguru handlers during tests to avoid noisy output."""
    logger.remove()
    yield
    logger.remove()


@pytest.fixture
def client() -> Generator[TestClient]:
    """Provide a synchronous TestClient that exercises the full ASGI lifespan."""
    with TestClient(app) as test_client:
        yield test_client
