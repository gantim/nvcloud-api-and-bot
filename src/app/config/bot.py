from pydantic_settings import BaseSettings


class BotSettings(BaseSettings):
    TOKEN: str
    WEBHOOK_URL: str

    class Config:
        env_file = '.env'
        env_prefix = "BOT_"
        extra = 'ignore'
