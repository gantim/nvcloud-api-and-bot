from logging import getLogger
from typing import Optional

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.domain.models.tg_user import TgUserInDB
from app.domain.repo.tg_user import TgUserRepository
from app.infra.database.models.tg_user import TgUser

logger = getLogger(__name__)

class SQLAlchemyTgUserRepository(TgUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def get(self, user_id: int) -> Optional[TgUserInDB]:
        stmt = select(TgUser).where(TgUser.chat_id == user_id)
        result = await self.session.execute(stmt)
        orm_tg_user = result.scalars().first()

        if orm_tg_user:
            return self._map_to_domain(orm_tg_user)
        return None

    async def update(self, tg_user: TgUserInDB) -> TgUserInDB:
        stmt = select(TgUser).where(TgUser.user_id == tg_user.user_id)
        result = await self.session.execute(stmt)
        orm_tg_user = result.scalars().first()

        if orm_tg_user:
            orm_tg_user.username = tg_user.username
            orm_tg_user.full_name = tg_user.full_name
            orm_tg_user.meta = tg_user.meta
            await self.session.flush()
            return self._map_to_domain(orm_tg_user)
        raise ValueError(f"Telegram user with ID {tg_user.user_id} not found")

    async def search(
        self,
        is_superuser: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[TgUserInDB]:
        stmt = select(TgUser).options(selectinload(TgUser.user))

        conditions = []
        if is_superuser is not None:
            conditions.append(TgUser.is_superuser == is_superuser) # type: ignore

        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = stmt.limit(limit).offset(offset)

        result = await self.session.execute(stmt)
        return [self._map_to_domain(c) for c in result.scalars()]

    async def get_by_username(self, username: str) -> Optional[TgUserInDB]:
        stmt = select(TgUser).where(TgUser.username == username)
        result = await self.session.execute(stmt)
        orm_tg_user = result.scalars().first()

        if orm_tg_user:
            return self._map_to_domain(orm_tg_user)
        return None

    async def add(self, tg_user: TgUserInDB) -> TgUserInDB:
        orm_tg_user = self._map_to_orm(tg_user)
        self.session.add(orm_tg_user)
        await self.session.flush()

        # Update the domain model with any changes from the ORM
        tg_user.meta = orm_tg_user.meta or {}
        return tg_user

    async def delete(self, user_id: int) -> None:
        orm_tg_user = await self.get(user_id)
        if orm_tg_user:
            await self.session.delete(orm_tg_user)

    def _map_to_domain(self, orm_tg_user: TgUser) -> TgUserInDB:
        return TgUserInDB(
            is_superuser=orm_tg_user.is_superuser,
            chat_id=orm_tg_user.chat_id,
            user_id=orm_tg_user.user_id, # type: ignore
            username=orm_tg_user.username,
            full_name=orm_tg_user.full_name,
            meta=orm_tg_user.meta or {},
            created_at=orm_tg_user.created_at,
            updated_at=orm_tg_user.updated_at,
            is_deleted=orm_tg_user.is_deleted
        )

    def _map_to_orm(self, tg_user: TgUserInDB) -> TgUser:
        return TgUser(
            is_superuser=tg_user.is_superuser,
            chat_id=tg_user.chat_id,
            user_id=tg_user.user_id,
            username=tg_user.username,
            full_name=tg_user.full_name,
            meta=tg_user.meta,
            created_at=tg_user.created_at,
            updated_at=tg_user.updated_at,
            is_deleted=tg_user.is_deleted if tg_user.is_deleted is not None else False
        )
