from aiogram import F
from aiogram.enums.chat_type import ChatType
from aiogram.filters import Command
from aiogram.filters.logic import or_f
from aiogram.types import Message

from app.bot.routers import BaseRouter
from app.domain.models.tg_user import TgUserInDB
from app.domain.uow.abstract import AbstractUnitOfWork


class AdminRouter(BaseRouter):
    chat_types = ChatType.PRIVATE

    def setup_handlers(self):
        @self.message(or_f(Command('post'), F.text.startswitch('/post'), F.caption.startswitch('/post')))
        async def send_post_handler(event: Message, uow: AbstractUnitOfWork, user: TgUserInDB):
            if not user.is_superuser:
                return
            text = None
            if event.text:
                text = event.text.replace('/post', '')
            elif event.caption:
                text = event.caption.replace('/post', '')

            if not text:
                return

            users = await uow.tg_users_repo.search()

            for user in users:
                if event.photo:
                    await event.bot.send_photo(user.chat_id, event.photo[-1].file_id, caption=text) # type: ignore
                elif event.text:
                    await event.bot.send_message(user.chat_id, text) # type: ignore
