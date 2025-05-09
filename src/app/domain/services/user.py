from app.domain.models.user import UserInDB
from app.domain.uow.abstract import AbstractUnitOfWork


class UserService:
    def __init__(self, uow: AbstractUnitOfWork):
        self._uow = uow

    async def create_user(self, username: str, email: str, hashed_password: str, full_name: str):
        async with self._uow:
            user = UserInDB(
                username=username,
                email=email,
                full_name=full_name,
                hashed_password=hashed_password
            )
            return await self._uow.user_repo.add(user)

    async def get_user_by_username(self, username: str):
        async with self._uow:
            return await self._uow.user_repo.get_by_username(username)

    async def get_user_by_email(self, email: str):
        async with self._uow:
            return await self._uow.user_repo.get_by_email(email)
