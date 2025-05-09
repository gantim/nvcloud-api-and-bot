from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.security.jwt import JWTService, get_jwt_service
from app.domain.models.user import UserInDB
from app.domain.services.user import UserService
from app.presentation.dependencies.services import get_user_service
from app.presentation.exceptions.auth import CredentialsException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

async def validate_and_get_username(
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_service: Annotated[JWTService, Depends(get_jwt_service)]
) -> str:
    if username := jwt_service.verify_token(token):
        return username
    raise CredentialsException

async def get_authenticated_user(
    username: str,
    user_service: UserService
) -> UserInDB:
    if user := await user_service.get_user_by_username(username):
        return user
    raise CredentialsException

async def get_current_user(
    username: Annotated[str, Depends(validate_and_get_username)],
    user_service: Annotated[UserService, Depends(get_user_service)]
) -> UserInDB:
    return await get_authenticated_user(username, user_service)
