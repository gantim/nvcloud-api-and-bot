from datetime import datetime, timedelta, timezone
from typing import Any

from jwt import PyJWTError, decode, encode

from app.config import create_settings
from app.config.api import APISettings


class JWTService:
    def __init__(self, settings: APISettings):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.token_expire_minutes = timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)

    def create_access_token(self, data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        now = datetime.now(timezone.utc)
        expire = now + (expires_delta if expires_delta else self.token_expire_minutes)
        to_encode.update({
            "exp": expire,
            "iat": now
        })
        return encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> str | None:
        try:
            payload = decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={"verify_exp": True}
            )
            return str(payload.get("username"))
        except PyJWTError:
            return None

def get_jwt_service() -> JWTService:
    return JWTService(create_settings().api_settings)
