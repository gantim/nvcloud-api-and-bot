from logging import getLogger
from typing import Any, Awaitable, Callable
from uuid import UUID

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update, User

from app.domain.models.tg_user import TgUserInDB
from app.domain.uow.abstract import AbstractUnitOfWork


def is_valid_uuid4(uuid_str: str) -> UUID: # type: ignore
    try:
        uuid_obj = UUID(uuid_str)
        if uuid_obj.version == 4 and str(uuid_obj) == uuid_str:
            return uuid_obj
    except ValueError:
        return False # type: ignore


logger = getLogger(__name__)


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:
        uow: AbstractUnitOfWork = data['uow']
        user: User = data['event_from_user']

        tg_user = await uow.tg_users_repo.get(user.id)
        if tg_user is None and isinstance(event, Update) and event.message and event.message.text:
            text = event.message.text
            if text.startswith('/start') and len( text.split()) == 2 and (user_id := is_valid_uuid4(text.split()[1])):
                user_db = await uow.user_repo.get(user_id)
                if user_db and user_db.telegram_id and user_db.telegram_id != user.id:
                    return
                tg_user = await uow.tg_users_repo.add(
                    TgUserInDB( # type: ignore
                        chat_id=user.id,
                        user_id=user_id,
                        username=user.username,
                        full_name=user.full_name,
                    )
                )

        data.update(user=tg_user, user_in_db=None)

        return await handler(event, data)
