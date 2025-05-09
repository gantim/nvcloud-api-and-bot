from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from app.config.redis import RedisSettings


def create_redis_storage(settings: RedisSettings) -> RedisStorage:
    redis_client = Redis.from_url(settings.DATABASE_URL)
    redis_storage = RedisStorage(
        redis_client,
        key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True)
        )

    return redis_storage
