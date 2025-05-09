from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI

from app.bot import create_bot_manager, create_dispatcher_manager, create_redis_storage
from app.config import create_settings
from app.infra.logging import setup_logging
from app.presentation.builder import get_api_builder

logger = getLogger(__name__)


def init() -> FastAPI:
    settings = create_settings()
    setup_logging(settings.logging_settings)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        bot_manager = create_bot_manager(settings.bot_settings)
        redis_storage = create_redis_storage(settings.redis_settings)

        dp_manager = create_dispatcher_manager(bot_manager, redis_storage)
        dp_manager.setup()

        await dp_manager.setup_bot()
        try:
            yield
        finally:
            await bot_manager.bot.session.close()

    api_builder = get_api_builder(settings.api_settings, lifespan)

    api_builder.build()

    return api_builder.api
