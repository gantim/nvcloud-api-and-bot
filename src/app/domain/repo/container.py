from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.models.container import ContainerInDB


class ContainerRepository(ABC):
    @abstractmethod
    async def get(self, id: UUID) -> Optional[ContainerInDB]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_vmid(self, vmid: int) -> Optional[ContainerInDB]:
        raise NotImplementedError

    @abstractmethod
    async def search(
        self,
        name: Optional[str] = None,
        owner_id: Optional[UUID] = None,
        is_template: Optional[bool] = None,
        tags: Optional[List[str]] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[ContainerInDB]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, container: ContainerInDB) -> ContainerInDB:
        raise NotImplementedError

    @abstractmethod
    async def update(self, container: ContainerInDB) -> ContainerInDB:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_vmid(self, vmid: int) -> None:
        raise NotImplementedError
