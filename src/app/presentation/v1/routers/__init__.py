from fastapi import APIRouter, FastAPI


def setup_routers(app: FastAPI) -> None:
    from .bot_routers import setup_bot_routers
    from .container_routers import setup_container_routers
    from .user_routers import setup_user_routers

    router = APIRouter(prefix='/api/v1')
    setup_user_routers(router)
    setup_container_routers(router)
    setup_bot_routers(router)

    app.include_router(router)
