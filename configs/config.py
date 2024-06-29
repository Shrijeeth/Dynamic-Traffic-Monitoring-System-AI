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
