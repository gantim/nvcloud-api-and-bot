from abc import abstractmethod
from uuid import UUID

from app.domain.models.user import UserInDB

from .base import BaseRepository


class UserRepository(BaseRepository[UserInDB, UUID]):
    @abstractmethod
    async def get_by_username(self, username: str) -> UserInDB | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> UserInDB | None:
        raise NotImplementedError
