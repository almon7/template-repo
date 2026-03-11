import sys

from loguru import logger

from app.settings import settings

_DEV_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green>"
    " | <level>{level: <8}</level>"
    " | <cyan>{name}</cyan>:<cyan>{line}</cyan>"
    " - <level>{message}</level>"
)


def configure_logging() -> None:
    """Configure loguru: remove the default handler and add a structured one.

    In production, logs are serialised to JSON so they can be ingested by log aggregation systems (Datadog, CloudWatch,
    Google Cloud Logging, …). In development, a human-readable coloured format is used instead.
    """
    logger.remove()
    if settings.environment == "production":
        # serialize=True emits newline-delimited JSON records.
        logger.add(sys.stderr, level=settings.log_level, serialize=True)
    else:
        logger.add(
            sys.stderr,
            level=settings.log_level,
            format=_DEV_FORMAT,
            colorize=sys.stderr.isatty(),
        )
