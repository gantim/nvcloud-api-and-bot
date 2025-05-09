from typing import Protocol

from app.domain.models.user import UserInDB
from app.domain.schemas.user import UserProfile


class ProfileUserUseCase(Protocol):
    def __init__(self, user: UserInDB): ...

    async def __call__(self) -> UserProfile: ...
