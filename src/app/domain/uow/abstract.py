from abc import ABC, abstractmethod

from app.domain.repo.container import ContainerRepository
from app.domain.repo.tg_user import TgUserRepository
from app.domain.repo.ticket_container import TicketContainerRepository
from app.domain.repo.user import UserRepository


class AbstractUnitOfWork(ABC):
    @property
    @abstractmethod
    def user_repo(self) -> UserRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def container_repo(self) -> ContainerRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def ticket_container_repo(self) -> TicketContainerRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def tg_users_repo(self) -> TgUserRepository:
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> 'AbstractUnitOfWork':
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, traceback):
        raise NotImplementedError
