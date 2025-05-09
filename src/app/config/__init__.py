from functools import lru_cache

from .settings import Settings


@lru_cache
def create_settings() -> Settings:
    return Settings()
