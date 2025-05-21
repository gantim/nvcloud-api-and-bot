'''from app.domain.models.tg_user import TgUserInDB
from app.domain.models.user import UserInDB
from app.domain.uow.abstract import AbstractUnitOfWork


class TgUserService:
    def __init__(self, uow: AbstractUnitOfWork):
        self._uow = uow

    async def create_user(self, user_id: str, username: str):
        async with self._uow:
            return await self._uow.user_repo.add()
'''
