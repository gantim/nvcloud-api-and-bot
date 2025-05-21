from aiogram import Dispatcher

from app.infra.database.uow import get_uow

from .container_service_middleware import ContainerMiddleware
from .uow_middleware import UoWMiddleware
from .user_middleware import UserMiddleware


def connect_update_middlewares(dp: Dispatcher):
    dp.update.middleware(UoWMiddleware(get_uow()))
    dp.update.middleware(UserMiddleware())
    dp.update.middleware(ContainerMiddleware())
