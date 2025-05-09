from aiogram import Dispatcher

from .base import BaseRouter as BaseRouter
from .private.user_router import UserRouter


def setup_routers(dp: Dispatcher):
    dp.include_router(UserRouter())
