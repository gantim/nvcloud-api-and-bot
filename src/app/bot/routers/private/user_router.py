from aiogram.enums.chat_type import ChatType
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.bot.locales import ru
from app.bot.routers import BaseRouter


class UserRouter(BaseRouter):
    chat_types = ChatType.PRIVATE

    def setup_handlers(self):
        @self.message(CommandStart())
        async def start_handler(event: Message):
            await event.answer(ru.START_TEXT)
