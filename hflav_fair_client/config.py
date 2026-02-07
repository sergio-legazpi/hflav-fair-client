from enum import Enum
import os


class EnvironmentVariables(Enum):
    """Enumeration of environment variable keys."""

    HFLAV_CACHE_NAME = "HFLAV_CACHE_NAME"
    HFLAV_CACHE_EXPIRE_AFTER = "HFLAV_CACHE_EXPIRE_AFTER"


class Config:
    """Class to manage environment variables for configuration."""

    @staticmethod
    def get_variable(key: EnvironmentVariables, default: str) -> str:
        return os.getenv(key.value, default)
