# pylint: disable=too-few-public-methods

"""
Environment Variable Config module
"""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings class to manage environment variables
    """

    ENVIRONMENT: str = "development"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_USERNAME: str | None = None
    REDIS_PASSWORD: str | None = None
    REDIS_DB: int = 0

    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = "username"
    SMTP_PASSWORD: str = "password"

    class Config:
        """
        Config class to manage environment variable files
        """

        env_file = ".env" if os.getenv("ENVIRONMENT") != "development" else ".env.test"


@lru_cache
def get_settings():
    """
    This function retrieves and returns the settings object.

    Returns:
        Settings: The settings object.
    """
    return Settings()
