from pydantic_settings import BaseSettings


class APISettings(BaseSettings):
    API_PREFIX: str = "api"
    API_VERSION: str = "v1"
    SECRET_KEY: str = 'Se'
    ALGORITHM: str = 'HS256'
    DEBUG: bool = True
    ALLOWED_HOSTS: list[str] = ['*']
    CORS_ORIGINS: list[str] = ['*']
    TOKEN_EXPIRE_MINUTES: int = 30

    TITLE: str = 'NV CLOUD API'
    DESCRIPTION: str = 'meow'
    VERSION: str = '0.1.0'

    class Config:
        env_file = '.env'
        env_prefix = "API_"
        extra = 'ignore'
