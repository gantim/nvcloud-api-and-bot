from abc import abstractmethod
from typing import Optional

from app.domain.models.tg_user import TgUserInDB

from .base import BaseRepository


class TgUserRepository(BaseRepository[TgUserInDB, int]):
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[TgUserInDB]:
        raise NotImplementedError

    @abstractmethod
    async def search(self, is_superuser: bool | None = None, limit: int = 100, offset: int = 0) -> list[TgUserInDB]:
        raise NotImplementedError
