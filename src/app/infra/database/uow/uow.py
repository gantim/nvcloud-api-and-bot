from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.domain.uow.abstract import AbstractUnitOfWork
from app.infra.database.repositories.container import SQLAlchemyContainerRepository
from app.infra.database.repositories.tg_user import SQLAlchemyTgUserRepository
from app.infra.database.repositories.ticket_container import (
    SQLAlchemyTicketContainerRepository,
)
from app.infra.database.repositories.user import SQLAlchemyUserRepository


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory
        self.session: AsyncSession = None # type: ignore
        self._user_repo: SQLAlchemyUserRepository = None # type: ignore
        self._container_repo: SQLAlchemyContainerRepository = None # type: ignore
        self._ticket_container_repo: SQLAlchemyTicketContainerRepository = None # type: ignore
        self._tg_users_repo: SQLAlchemyTgUserRepository = None # type: ignore

    @property
    def user_repo(self):
        return self._user_repo

    @property
    def container_repo(self):
        return self._container_repo

    @property
    def ticket_container_repo(self):
        return self._ticket_container_repo

    @property
    def tg_users_repo(self):
        return self._tg_users_repo

    async def __aenter__(self):
        self.session = self._session_factory()
        self._user_repo = SQLAlchemyUserRepository(self.session)
        self._container_repo = SQLAlchemyContainerRepository(self.session)
        self._ticket_container_repo = SQLAlchemyTicketContainerRepository(self.session)
        self._tg_users_repo = SQLAlchemyTgUserRepository(self.session)
        await self.session.begin()
        return self

    async def __aexit__(self, exc_type, exc_val, traceback):
        if exc_type:
            await self.session.rollback()

        await self.session.commit()
        await self.session.close()
        return False
