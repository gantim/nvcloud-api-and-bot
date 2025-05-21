from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.domain.schemas.auth import Token, VerifyUser
from app.domain.use_cases.auth_user import AuthUseCase
from app.presentation.dependencies.auth.jwt import validate_and_get_username
from app.presentation.dependencies.use_cases import (
    get_login_user_use_case,
    get_oauth_use_case,
    get_register_user_use_case,
)


def get_auth_router() -> APIRouter:
    router = APIRouter(prefix='/auth', tags=['Authentication (OAuth2)'])

    @router.post('/token/verify')
    async def token_verify(username: Annotated[str, Depends(validate_and_get_username)]):
        return VerifyUser(username=username)

    @router.post('/token', response_model=Token)
    async def oauth_token(use_case: Annotated[AuthUseCase, Depends(get_oauth_use_case)]) -> Token:
        return await use_case()

    @router.post('/signup', status_code=status.HTTP_201_CREATED)
    async def signup_handler(use_case: Annotated[AuthUseCase, Depends(get_register_user_use_case)]) -> Token:
        return await use_case()

    @router.post('/login', status_code=status.HTTP_200_OK)
    async def login_handler(use_case: Annotated[AuthUseCase, Depends(get_login_user_use_case)]) -> Token:
        return await use_case()


    return router
