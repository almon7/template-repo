from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sample_env_var: str


settings = Settings()
