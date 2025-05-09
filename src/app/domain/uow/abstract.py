from abc import ABC, abstractmethod

from app.domain.repo.user import UserRepository


class AbstractUnitOfWork(ABC):
    @property
    @abstractmethod
    def user_repo(self) -> UserRepository:
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> 'AbstractUnitOfWork':
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, traceback):
        raise NotImplementedError
