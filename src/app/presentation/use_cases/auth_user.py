from fastapi.security import OAuth2PasswordRequestForm

from app.core.security.jwt import JWTService
from app.core.security.password import get_password_hash, verify_password
from app.domain.schemas.auth import LogIn, SignUp, Token
from app.domain.services.user import UserService
from app.presentation.exceptions.auth import (
    EmailBusy,
    InvalidPassword,
    UserAlreadySignUp,
    UserNotFound,
)


class BaseAuthUseCase:
    def __init__(self, user_service: UserService, jwt_service: JWTService, request: LogIn | SignUp | None = None):
        self.request = request
        self.user_service = user_service
        self.jwt_service = jwt_service

    def _create_token_by_username(self, username: str) -> Token:
        token = self.jwt_service.create_access_token(data={'username': username})
        return Token(access_token=token, token_type='bearer')

class RegisterUserUseCase(BaseAuthUseCase):
    request: SignUp
    async def __call__(self) -> Token:
        if await self.user_service.get_user_by_username(self.request.username):
            raise UserAlreadySignUp

        if await self.user_service.get_user_by_email(self.request.email):
            raise EmailBusy

        hashed_password = get_password_hash(self.request.password)

        user = await self.user_service.create_user(
            username=self.request.username,
            email=self.request.email,
            hashed_password=hashed_password,
            full_name=self.request.full_name
        )

        return self._create_token_by_username(user.username)

class LoginUserUseCase(BaseAuthUseCase):
    request: LogIn
    async def __call__(self) -> Token:
        if not (user := await self.user_service.get_user_by_username(self.request.username)):
            raise UserNotFound

        if not verify_password(self.request.password, user.hashed_password):
            raise InvalidPassword

        return self._create_token_by_username(user.username)

class OAuthUserUseCase(BaseAuthUseCase):
    async def __call__(self, form_data: OAuth2PasswordRequestForm) -> Token:

        if not (user := await self.user_service.get_user_by_username(form_data.username)):
            raise UserNotFound

        print(f"Input password: {form_data.password}")
        print(f"Stored hash: {user.hashed_password}")
        print(f"Verify result: {verify_password(form_data.password, user.hashed_password)}")

        if not verify_password(form_data.password, user.hashed_password):
            raise InvalidPassword

        return self._create_token_by_username(user.username)
