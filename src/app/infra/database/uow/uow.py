from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.domain.uow.abstract import AbstractUnitOfWork
from app.infra.database.repositories.user import SQLAlchemyUserRepository


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory
        self.session: AsyncSession = None # type: ignore
        self._user_repo: SQLAlchemyUserRepository = None # type: ignore

    @property
    def user_repo(self):
        return self._user_repo

    async def __aenter__(self):
        self.session = self._session_factory()
        self._user_repo = SQLAlchemyUserRepository(self.session)
        await self.session.begin()
        return self

    async def __aexit__(self, exc_type, exc_val, traceback):
        if exc_type:
            await self.session.rollback()
        else:
            if self.session.dirty or self.session.new:
                await self.session.commit()
        await self.session.close()
        return False
