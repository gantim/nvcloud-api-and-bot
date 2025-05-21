from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.domain.models.tg_user import TgUserInDB
from app.domain.services.container import ContainerService
from app.domain.uow.abstract import AbstractUnitOfWork
from app.presentation.dependencies.proxmox import get_proxmox_provider


class ContainerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:

        user: TgUserInDB = data['user'] # type: ignore
        if user and user.user_id:
            uow: AbstractUnitOfWork = data['uow']
            user_in_db = await uow.user_repo.get(user.user_id)
            data.update(user_in_db=user_in_db, container_service=ContainerService(uow, get_proxmox_provider(), user_in_db)) # type: ignore
        return await handler(event, data)
