from typing import Annotated

from aiogram.types import Update
from fastapi import APIRouter, Depends, Response, status

from app.bot.builder.dispatcher_manager import DispatcherManager


def get_bot_webhook_router() -> APIRouter:
    router = APIRouter(prefix='/bot', tags=['WebHook Bot'])

    @router.post('/webhook', status_code=status.HTTP_200_OK, response_model=None, include_in_schema=False)
    async def profile_handler(update: Update, dm: Annotated[DispatcherManager, Depends(DispatcherManager.get_instance)]):
        await dm.feed_update(update)
        return Response(status_code=status.HTTP_200_OK)

    return router
