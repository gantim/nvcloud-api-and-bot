from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)  # Domain model type
K = TypeVar("K")  # ID type (int, str, UUID etc.)

class BaseRepository(ABC, Generic[T, K]):
    @abstractmethod
    async def get(self, id: K) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def add(self, entity: T) -> T:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: T) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: K) -> None:
        raise NotImplementedError
