from aiogram.fsm.storage.base import BaseStorage

from app.config.bot import BotSettings

from .builder.bot_manager import BotManager
from .builder.dispatcher_manager import DispatcherManager
from .builder.instance_redis_storage import create_redis_storage as create_redis_storage


def create_dispatcher_manager(bot_manager: BotManager, storage: BaseStorage) -> DispatcherManager:
    return DispatcherManager(
        storage=storage,
        bot_manager=bot_manager
    )

def create_bot_manager(settings: BotSettings) -> BotManager:
    return BotManager(settings.WEBHOOK_URL, settings.TOKEN)

