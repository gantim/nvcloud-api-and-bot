from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    DB: int = 1
    USER: str = 'nvcloud'
    PASSWORD: str = '1234'
    HOST: str = 'localhost'
    PORT: int = 1234

    @property
    def DATABASE_URL(self) -> str:
        #auth_part = f"{self.USER}:{self.PASSWORD}@" if self.USER and self.PASSWORD else ""
        db_part = f"/{self.DB}" if self.DB else ""
        return f"redis://{self.HOST}:{self.PORT}{db_part}"

    class Config:
        env_file = ".env"
        env_prefix = 'REDIS_'
        extra = "ignore"
