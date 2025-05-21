from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.domain.uow.abstract import AbstractUnitOfWork


class UoWMiddleware(BaseMiddleware):
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self._uow = uow

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:
        async with self._uow:
            data['uow'] = self._uow
            result = await handler(event, data)

        return result
