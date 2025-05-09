from typing import Generic, Optional, Type, TypeVar

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.base import BaseEntity
from app.domain.repo.base import BaseRepository
from app.infra.database.models.base import Base

TModel = TypeVar("TModel", bound=BaseEntity)  # Domain model type
TDBModel = TypeVar("TDBModel", bound=Base)  # SQLAlchemy model type
K = TypeVar("K")  # ID type


class SQLAlchemyRepository(BaseRepository[TModel, K], Generic[TModel, TDBModel, K]):
    def __init__(
        self,
        session: AsyncSession,
        domain_model: Type[TModel],
        db_model: Type[TDBModel]
    ):
        self._session = session
        self._domain_model = domain_model
        self._db_model = db_model

    async def get(self, id: K) -> Optional[TModel]:
        result = await self._session.execute(
            select(self._db_model).where(self._db_model.id == id)
        )
        db_entity = result.scalars().first()
        return self._to_domain(db_entity) if db_entity else None

    async def add(self, entity: TModel) -> TModel:
        db_entity = self._to_db(entity)
        self._session.add(db_entity)
        await self._session.flush()
        await self._session.refresh(db_entity)
        return self._to_domain(db_entity)

    async def update(self, entity: TModel) -> TModel:
        db_entity = self._to_db(entity)
        await self._session.execute(
            update(self._db_model)
            .where(self._db_model.id == entity.id)
            .values(**db_entity.__dict__)
        )
        return entity

    async def delete(self, id: K) -> None:
        await self._session.execute(
            delete(self._db_model).where(self._db_model.id == id)
        )

    def _to_domain(self, db_entity: TDBModel) -> TModel:
        return self._domain_model.model_validate(db_entity.__dict__)

    def _to_db(self, domain_entity: TModel) -> TDBModel:
        return self._db_model(**domain_entity.model_dump())
