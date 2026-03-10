from loguru import logger

from app.log import configure_logging


def main() -> None:
    configure_logging()
    logger.info("Hello, World!")


if __name__ == "__main__":
    main()
