from fastapi import APIRouter

from .bot_webhook_router import get_bot_webhook_router


def setup_bot_routers(app: APIRouter) -> None:
    app.include_router(get_bot_webhook_router())
