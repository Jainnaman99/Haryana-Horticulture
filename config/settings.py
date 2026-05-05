from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    # App Info
    PROJECT_NAME: str = "Horticulture Department API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Horticulture Department API"

    # DB Config (from .env)
    DB_HOST: str
    DB_PORT: int = 1433
    DB_NAME: str
    DB_INTEGRATED_AUTH: bool = True

    DB_USER: str | None = None
    DB_PASSWORD: str | None = None

    # Other config
    DEBUG: bool = True
    LOCALHOST_UI_BASE_URL: str

    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    MAX_LOGIN_ATTEMPTS: int = 5

    ALLOWED_HOSTS: List[str] = ["*"]

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False
    )


@lru_cache()
def get_settings():
    return Settings()