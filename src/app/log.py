import sys

from loguru import logger

from app.settings import settings


def configure_logging() -> None:
    """Configure loguru: remove the default handler and add a structured one."""
    logger.remove()
    logger.add(
        sys.stderr,
        level=settings.log_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green>"
            " | <level>{level: <8}</level>"
            " | <cyan>{name}</cyan>:<cyan>{line}</cyan>"
            " - <level>{message}</level>"
        ),
        colorize=sys.stderr.isatty(),
    )
