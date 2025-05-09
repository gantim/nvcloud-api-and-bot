from pydantic_settings import BaseSettings

from app.config.api import APISettings
from app.config.bot import BotSettings
from app.config.database import DatabaseSettings
from app.config.logging import LoggingSettings
from app.config.proxmox import ProxmoxSettings
from app.config.redis import RedisSettings


class Settings(BaseSettings):
    api_settings: APISettings = APISettings()
    database_settings: DatabaseSettings = DatabaseSettings() # type: ignore
    logging_settings: LoggingSettings = LoggingSettings()
    proxmox_settings: ProxmoxSettings = ProxmoxSettings() # type: ignore
    redis_settings: RedisSettings = RedisSettings() # type: ignore
    bot_settings: BotSettings = BotSettings() # type: ignore
    DEV: bool = True

    class Config:
        env_file = '.env'
        extra = 'ignore'
