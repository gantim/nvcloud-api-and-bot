from contextlib import asynccontextmanager
from typing import Annotated, AsyncContextManager, AsyncIterator

from fastapi import Depends

from app.domain.models.user import UserInDB
from app.domain.providers.container import ContainerAPIProvider
from app.domain.services.container import ContainerService
from app.domain.uow.abstract import AbstractUnitOfWork
from app.infra.database.uow import get_uow
from app.infra.proxmox import create_provider
from app.infra.proxmox.proxmox_provider import ProxmoxProvider
from app.presentation.dependencies.auth.jwt import get_current_user


@asynccontextmanager
async def get_proxmox_provider() -> AsyncIterator[ProxmoxProvider]:
    provider = create_provider()
    try:
        await provider._ensure_session()
        yield provider
    finally:
        await provider.close()


def get_container_service(
    user: Annotated[UserInDB, Depends(get_current_user)],
    uow: Annotated[AbstractUnitOfWork, Depends(get_uow)],
    proxmox_provider: Annotated[AsyncContextManager[ContainerAPIProvider], Depends(get_proxmox_provider)]
):
    return ContainerService(uow, proxmox_provider, user)
