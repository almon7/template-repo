"""
Shared pytest fixtures and configuration.
Add fixtures here that are needed across multiple test modules.
"""

import pytest
from loguru import logger


@pytest.fixture(autouse=True)
def silence_logs():
    """Remove all loguru handlers during tests to avoid noisy output."""
    logger.remove()
    yield
    logger.remove()
