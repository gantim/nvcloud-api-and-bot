from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import create_settings

settings = create_settings().database_settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)

SessionFactory = async_sessionmaker( # type: ignore
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
