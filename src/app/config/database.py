from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    DB: str
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}"

    class Config:
        env_file = ".env"
        env_prefix = 'POSTGRES_'
        extra = "ignore"

