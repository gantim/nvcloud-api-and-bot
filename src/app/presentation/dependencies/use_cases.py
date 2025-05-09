from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security.jwt import JWTService, get_jwt_service
from app.domain.models.user import UserInDB
from app.domain.schemas.auth import LogIn, SignUp
from app.domain.services.user import UserService
from app.presentation.dependencies.auth.jwt import get_current_user
from app.presentation.use_cases.auth_user import LoginUserUseCase, RegisterUserUseCase
from app.presentation.use_cases.profile_user import ProfileUserUseCase

from .services import get_user_service


def get_login_user_use_case(
    request: LogIn,
    user_service: Annotated[UserService, Depends(get_user_service)],
    jwt_service: Annotated[JWTService, Depends(get_jwt_service)]
) -> LoginUserUseCase:
    return LoginUserUseCase(user_service, jwt_service, request)

def get_register_user_use_case(
    request: SignUp,
    user_service: Annotated[UserService, Depends(get_user_service)],
    jwt_service: Annotated[JWTService, Depends(get_jwt_service)]
) -> RegisterUserUseCase:
    return RegisterUserUseCase(user_service, jwt_service, request)

def get_oauth_use_case(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: Annotated[UserService, Depends(get_user_service)],
    jwt_service: Annotated[JWTService, Depends(get_jwt_service)]
) -> LoginUserUseCase:
    login_request = LogIn(
        username=form_data.username,
        password=form_data.password
    )
    return LoginUserUseCase(user_service, jwt_service, login_request)

def get_profile_user_use_case(
    user: Annotated[UserInDB, Depends(get_current_user)]
) -> ProfileUserUseCase:
    return ProfileUserUseCase(user)
