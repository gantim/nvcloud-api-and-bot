from logging import getLogger
from typing import Optional
from uuid import UUID

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.domain.models.container import ContainerInDB
from app.domain.repo.container import ContainerRepository
from app.infra.database.models.container import Container

logger = getLogger(__name__)


class SQLAlchemyContainerRepository(ContainerRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def get(self, id: UUID) -> Optional[ContainerInDB]:
        stmt = select(Container).where(Container.id == id)
        result = await self.session.execute(stmt)
        orm_container = result.scalars().first()

        if orm_container:
            return self._map_to_domain(orm_container)
        return None

    async def get_by_vmid(self, vmid: int) -> Optional[ContainerInDB]:
        stmt = select(Container).where(Container.proxmox_vmid == vmid).options(selectinload(Container.owner))
        result = await self.session.execute(stmt)
        orm_container = result.scalars().first()

        if orm_container:
            return self._map_to_domain(orm_container)
        return None

    async def search(
        self,
        name: Optional[str] = None,
        owner_id: Optional[UUID] = None,
        is_template: Optional[bool] = None,
        tags: Optional[list[str]] = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[ContainerInDB]:
        stmt = select(Container).options(selectinload(Container.owner))

        conditions = []
        if name:
            conditions.append(Container.name.ilike(f"%{name}%"))
        if owner_id:
            conditions.append(Container.owner_id == owner_id) # type: ignore
        if is_template is not None:
            conditions.append(Container.is_template == is_template) # type: ignore
        if tags:
            conditions.append(Container.tags.contains(tags)) # type: ignore

        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = stmt.limit(limit).offset(offset)

        result = await self.session.execute(stmt)
        return [self._map_to_domain(c) for c in result.scalars()]

    async def add(self, container: ContainerInDB) -> ContainerInDB:
        orm_container = self._map_to_orm(container)
        self.session.add(orm_container)
        await self.session.flush()

        container.id = orm_container.id
        container.created_at = orm_container.created_at

        return container

    async def update(self, container: ContainerInDB) -> ContainerInDB:
        orm_container = None
        if container.id:
            orm_container = await self._get_orm_container(container.id)
        if not orm_container:
            raise ValueError(f"Container with id {container.id} not found")

        # Обновляем только изменяемые поля
        orm_container.name = container.name
        orm_container.description = container.description
        orm_container.tags = container.tags # type: ignore
        orm_container.lxc_config = container.lxc_config # type: ignore
        orm_container.is_template = container.is_template
        orm_container.is_protected = container.is_protected

        await self.session.flush()
        return self._map_to_domain(orm_container)

    async def delete(self, id: UUID) -> None:
        orm_container = await self._get_orm_container(id)
        if orm_container:
            await self.session.delete(orm_container)

    async def delete_by_vmid(self, vmid: int) -> None:
        orm_container = await self._get_orm_container_by_vmid(vmid)
        if orm_container:
            await self.session.delete(orm_container)

    async def _get_orm_container_by_vmid(self, vmid: int) -> Optional[Container]:
        stmt = select(Container).where(Container.proxmox_vmid == vmid)
        result = await self.session.execute(stmt)
        return result.scalars().first()


    async def _get_orm_container(self, id: UUID) -> Optional[Container]:
        stmt = select(Container).where(Container.id == id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    def _map_to_domain(self, orm_container: Container) -> ContainerInDB:
        return ContainerInDB(
            id=orm_container.id,
            password=orm_container.password,
            proxmox_vmid=orm_container.proxmox_vmid,
            proxmox_node=orm_container.proxmox_node,
            name=orm_container.name,
            description=orm_container.description,
            tags=orm_container.tags,
            lxc_config=orm_container.lxc_config,
            owner_id=orm_container.owner_id,
            is_template=orm_container.is_template,
            is_protected=orm_container.is_protected,
            created_at=orm_container.created_at,
            # Если нужно включать связанные объекты
            owner_username=orm_container.owner.username if orm_container and hasattr(orm_container.owner, 'username') else None
        )

    def _map_to_orm(self, container: ContainerInDB) -> Container:
        return Container(
            id=container.id,
            password=container.password,
            proxmox_vmid=container.proxmox_vmid,
            proxmox_node=container.proxmox_node,
            name=container.name,
            description=container.description,
            tags=container.tags,
            lxc_config=container.lxc_config,
            owner_id=container.owner_id,
            is_template=container.is_template,
            is_protected=container.is_protected,
            created_at=container.created_at,
            last_modified=container.last_modified
        )
