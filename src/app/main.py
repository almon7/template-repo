from loguru import logger

from app.log import configure_logging
from app.settings import settings


def main() -> None:
    configure_logging()
    logger.info("Hello, World!")
    logger.info(f"Sample Env Var: {settings.sample_env_var}")


if __name__ == "__main__":
    main()
