from aiogram import Dispatcher

from .base import BaseRouter as BaseRouter
from .private.admin_router import AdminRouter
from .private.user_router import UserRouter


def setup_routers(dp: Dispatcher):
    dp.include_router(UserRouter())
    dp.include_router(AdminRouter())
