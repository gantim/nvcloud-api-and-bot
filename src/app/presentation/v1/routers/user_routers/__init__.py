from fastapi import APIRouter

from .auth_router import get_auth_router
from .user_router import get_user_router


def setup_user_routers(app: APIRouter) -> None:
    app.include_router(get_auth_router())
    app.include_router(get_user_router())
