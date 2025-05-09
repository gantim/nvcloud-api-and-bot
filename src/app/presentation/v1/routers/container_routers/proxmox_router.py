from typing import Annotated, AsyncContextManager

from fastapi import APIRouter, Depends, status

from app.domain.providers.container import ContainerAPIProvider
from app.domain.schemas.container.response import (
    ContainerInfo,
    ContainerTelemetry,
    CreateTicket,
)
from app.presentation.dependencies.proxmox import (
    get_proxmox_provider,
)


def get_proxmox_router() -> APIRouter:

    router = APIRouter(
        prefix='/proxmox',
        tags=['Proxmox Containers']
    )

    @router.get(
        '/container',
        status_code=status.HTTP_200_OK,
        summary="Get Container Info",
        description="Retrieve detailed information about a specific container."
    )
    async def get_container_info_handler(container_provider: Annotated[ContainerAPIProvider, Depends(get_proxmox_provider)]) -> ContainerInfo:
        return ContainerInfo(id=1, name='Ivan')

    @router.post(
        '/container',
        status_code=status.HTTP_201_CREATED,
        summary="Create New Container",
        description="Create a new container and return a ticket for tracking."
    )
    async def create_container_handler(container_provider: Annotated[AsyncContextManager[ContainerAPIProvider], Depends(get_proxmox_provider)]): # type: ignore
        async with container_provider as provider:
            CreateTicket(id=101)
            return await provider.create_container(
                'nvcloud',
                101,
                ostemplate="local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst",
                network_config={
                    "bridge": "vmbr0",
                    "ip": "192.168.100.100/24",
                    "gw": "192.168.100.1",
                    "dhcp": False
                })

    @router.delete(
        '/container',
        status_code=status.HTTP_200_OK,
        summary="Delete Container",
        description="Delete an existing container by its identifier."
    )
    async def delete_container_handler() -> None:
        return

    @router.get(
        '/container/telemetry',
        status_code=status.HTTP_200_OK,
        summary="Get Container Telemetry",
        description="Retrieve telemetry data and status for a specific container."
    )
    async def get_container_telemetry_handler() -> ContainerTelemetry:
        return # type: ignore

    @router.post(
        '/container/stop',
        status_code=status.HTTP_200_OK,
        summary="Stop Container",
        description="Stop a running container."
    )
    async def stop_container_handler() -> None:
        return

    @router.post(
        '/container/start',
        status_code=status.HTTP_200_OK,
        summary="Stop Container",
        description="Stop a running container."
    )
    async def start_container_handler() -> None:
        return

    @router.post(
        '/container/restart',
        status_code=status.HTTP_200_OK,
        summary="Restart Container",
        description="Restart a specific container."
    )
    async def restart_container_handler() -> None:
        return



    return router
