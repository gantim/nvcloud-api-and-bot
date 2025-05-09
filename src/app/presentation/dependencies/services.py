from typing import Annotated

from fastapi import Depends

from app.domain.services.user import UserService
from app.domain.uow.abstract import AbstractUnitOfWork
from app.infra.database.uow import get_uow


def get_user_service(
    uow: Annotated[AbstractUnitOfWork, Depends(get_uow)]
):
    return UserService(uow)
