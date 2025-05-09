from typing import Any, Protocol

from app.core.security.jwt import JWTService
from app.domain.repo.user import UserRepository
from app.domain.schemas.auth import LogIn, SignUp, Token


class AuthUseCase(Protocol):
    def __init__(self, request: LogIn | SignUp, user_provider: UserRepository, jwt_service: JWTService): ...

    async def __call__(self, *args: Any, **kwargs: dict[str, Any]) -> Token: ...
