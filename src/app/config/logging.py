import logging

from pydantic_settings import BaseSettings


class LoggingSettings(BaseSettings):
    LOG_LEVEL: int = logging.DEBUG
    LOG_FILE_PATH: str = "/var/log/app.log"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_TO_CONSOLE: bool = True
    LOG_TO_FILE: bool = True
    LOG_MAX_BYTES: int = 1000000
    LOG_BACKUP_COUNT: int = 5

    class Config:
        env_file = '.env'
        env_prefix = "LOGGING_"
        extra = 'ignore'

