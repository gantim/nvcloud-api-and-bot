from logging import getLogger
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.domain.models.user import UserInDB
from app.domain.repo.user import UserRepository
from app.infra.database.models.user import User

logger = getLogger(__name__)

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session = None) -> None:
        self.session: AsyncSession = session

    async def get(self, id: UUID):
        stmt = select(User).where(User.id == id)
        result = await self.session.execute(stmt)
        orm_user = result.scalars().first()

        if orm_user:
            return self._map_to_domain(orm_user)
        else:
            return None

    async def update(self, UserInDB) -> UserInDB: # type: ignore
        ...

    async def get_by_username(self, username: str) -> UserInDB | None:
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        orm_user = result.scalars().first()

        if orm_user:
            return self._map_to_domain(orm_user)
        else:
            return None

    async def get_by_email(self, email: str) -> UserInDB | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        orm_user = result.scalars().first()

        if orm_user:
            return self._map_to_domain(orm_user)
        else:
            return None


    async def add(self, user: UserInDB) -> UserInDB:
        orm_user = self._map_to_orm(user)
        self.session.add(orm_user)
        await self.session.flush()

        user.id = orm_user.id
        user.created_at = orm_user.created_at
        user.updated_at = orm_user.updated_at

        return user

    async def delete(self, id: UUID) -> None:
        orm_user = await self.get(id)
        if orm_user:
            await self.session.delete(orm_user)

    def _map_to_domain(self, orm_user: User) -> UserInDB:
        return UserInDB(
            id=orm_user.id,
            telegram_id=orm_user.tg_user.chat_id if orm_user.tg_user else None,
            username=orm_user.username,
            email=orm_user.email,
            full_name=orm_user.full_name or '',
            is_superuser=orm_user.is_superuser,
            created_at=orm_user.created_at,
            updated_at=orm_user.updated_at,
            hashed_password=orm_user.hashed_password
        )

    def _map_to_orm(self, user: UserInDB) -> User:
        return User(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_superuser=user.is_superuser,
            created_at=user.created_at,
            updated_at=user.updated_at,
            hashed_password=user.hashed_password
        )
