from logging import getLogger

from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from aiogram.types import Update

from app.bot.middlewares.update import connect_update_middlewares
from app.bot.routers import setup_routers

from .bot_manager import BotManager

logger = getLogger(__name__)

class DispatcherManager:
    _instance: 'DispatcherManager' = None # type: ignore

    def __init__(self, storage: BaseStorage, bot_manager: BotManager):
        if DispatcherManager._instance is not None:
            raise RuntimeError("DispatcherManager is a singleton class. Use get_instance().")
        self.bot_manager = bot_manager
        self.dispatcher = Dispatcher(storage=storage, name=__name__)
        DispatcherManager._instance = self

    @classmethod
    def get_instance(cls) -> 'DispatcherManager':
        if cls._instance is None:
            raise RuntimeError("DispatcherManager has not been initialized yet.")
        return cls._instance

    @classmethod
    def initialize(cls, storage: BaseStorage, bot_manager: BotManager) -> 'DispatcherManager':
        if cls._instance is None:
            cls(storage, bot_manager)
        return cls._instance

    def setup(self):
        self._setup_middlewares()
        self._setup_routers()
        logger.info("Dispatcher Manager initialized")

    async def setup_bot(self):
        await self.bot_manager.create_bot()

    def _setup_middlewares(self):
        connect_update_middlewares(self.dispatcher)

    def _setup_routers(self):
        setup_routers(self.dispatcher)

    async def feed_update(self, update: Update) -> None:
        try:
            await self.dispatcher.feed_update( # type: ignore
                self.bot_manager.bot, # type: ignore
                update
            )
        except Exception as e:
            logger.error(f"Update processing error: {str(e)}")
