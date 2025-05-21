from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.domain.models.ticket_container import TicketContainerInDB


class TicketContainerRepository(ABC):
    @abstractmethod
    async def get(self, id: UUID) -> Optional[TicketContainerInDB]:
        raise NotImplementedError

    @abstractmethod
    async def search(self, limit: int = 100, offset: int = 0) -> list[TicketContainerInDB]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, container: TicketContainerInDB) -> TicketContainerInDB:
        raise NotImplementedError

    @abstractmethod
    async def update(self, container: TicketContainerInDB) -> TicketContainerInDB:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: UUID) -> None:
        raise NotImplementedError
