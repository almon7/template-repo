from loguru import logger

from app.settings import settings


def main():
    logger.info("Hello, World!")
    logger.info(f"Sample Env Var: {settings.sample_env_var}")


if __name__ == "__main__":
    main()
