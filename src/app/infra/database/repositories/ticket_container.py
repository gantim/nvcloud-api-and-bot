from logging import getLogger
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.domain.models.ticket_container import TicketContainerInDB
from app.domain.repo.ticket_container import TicketContainerRepository
from app.infra.database.models.ticket_container import TicketContainer

logger = getLogger(__name__)


class SQLAlchemyTicketContainerRepository(TicketContainerRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def get(self, id: UUID) -> Optional[TicketContainerInDB]:
        stmt = select(TicketContainer).where(TicketContainer.id == id).options(selectinload(TicketContainer.owner))
        result = await self.session.execute(stmt)
        orm_container = result.scalars().first()

        if orm_container:
            return self._map_to_domain(orm_container)
        return None

    async def search(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> list[TicketContainerInDB]:
        stmt = select(TicketContainer).options(selectinload(TicketContainer.owner))

        stmt = stmt.limit(limit).offset(offset)

        result = await self.session.execute(stmt)
        return [self._map_to_domain(c) for c in result.scalars()]

    async def add(self, container: TicketContainerInDB) -> TicketContainerInDB:
        orm_container = self._map_to_orm(container)
        self.session.add(orm_container)
        await self.session.flush()

        container.id = orm_container.id
        container.created_at = orm_container.created_at

        return container

    async def update(self, container: TicketContainerInDB) -> TicketContainerInDB:
        orm_container = None
        if container.id:
            orm_container = await self._get_orm_container(container.id)
        if not orm_container:
            raise ValueError(f"Container with id {container.id} not found")

        orm_container.name = container.name
        orm_container.closed = container.closed

        await self.session.flush()
        return self._map_to_domain(orm_container)

    async def delete(self, id: UUID) -> None:
        orm_container = await self._get_orm_container(id)
        if orm_container:
            await self.session.delete(orm_container)

    async def _get_orm_container(self, id: UUID) -> Optional[TicketContainer]:
        stmt = select(TicketContainer).where(TicketContainer.id == id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    def _map_to_domain(self, orm_container: TicketContainer) -> TicketContainerInDB:
        return TicketContainerInDB(
            id=orm_container.id,
            name=orm_container.name,
            ram_bytes=orm_container.ram_bytes,
            cpu_cores=orm_container.cpu_cores,
            rom_bytes=orm_container.rom_bytes,
            owner_id=orm_container.owner_id,
            closed=orm_container.closed,
            created_at=orm_container.created_at,
            owner_username=orm_container.owner.username if orm_container and hasattr(orm_container.owner, 'username') else None
        )

    def _map_to_orm(self, container: TicketContainerInDB) -> TicketContainer:
        return TicketContainer(
            proxmox_node='nvcloud',
            id=container.id,
            name=container.name,
            ram_bytes=container.ram_bytes,
            cpu_cores=container.cpu_cores,
            rom_bytes=container.rom_bytes,
            owner_id=container.owner_id,
            created_at=container.created_at,
            closed=container.closed
        )
