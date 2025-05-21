from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, status

from app.domain.models.ticket_container import TicketContainerInDB
from app.domain.schemas.container.request import CreateContainer
from app.domain.schemas.container.response import (
    ContainerAdminInfo,
    ContainerInfo,
    ContainerTelemetry,
    CreateTicket,
)
from app.domain.services.container import ContainerService
from app.presentation.dependencies.proxmox import get_container_service


def get_proxmox_router() -> APIRouter: # noqa: C901

    router = APIRouter(
        prefix='/proxmox',
        tags=['Proxmox Containers']
    )

    @router.get(
        '/container',
        status_code=status.HTTP_200_OK,
        summary="Get Containers Info",
        description="Retrieve summary information about a containers."
    )
    async def get_container_info(container_service: Annotated[ContainerService, Depends(get_container_service)]) -> list[ContainerInfo]:
        return await container_service.get_containers()

    @router.post(
        '/container',
        status_code=status.HTTP_201_CREATED,
        summary="Create New Container",
        description="Create a new container and return a ticket for tracking."
    )
    async def create_container(container: CreateContainer, container_service: Annotated[ContainerService, Depends(get_container_service)]) -> ContainerInfo:
        return await container_service.create_container(container)

    @router.post(
        '/container/ticket',
        status_code=status.HTTP_201_CREATED,
        summary="Create Container Ticket",
        description="Create a ticket for container creation."
    )
    async def create_ticket_container(container: CreateContainer, container_service: Annotated[ContainerService, Depends(get_container_service)]) -> CreateTicket:
        return await container_service.create_ticket_container(container)

    @router.delete(
        '/container/ticket/{id:str}',
        status_code=status.HTTP_200_OK,
        summary="Delete Container",
        description="Delete an existing container by its identifier."
    )
    async def delete_ticket_container(id: UUID, container_service: Annotated[ContainerService, Depends(get_container_service)]) -> None:
        await container_service.delete_ticket_container(id)

    @router.get(
        '/container/ticket',
        status_code=status.HTTP_200_OK,
        summary="Get all Container Tickets",
        description="Get a tickets for container creation."
    )
    async def get_tickets_container(container_service: Annotated[ContainerService, Depends(get_container_service)]) -> list[TicketContainerInDB]:
        return await container_service.get_tickets_container()

    @router.post(
        '/container/stop',
        status_code=status.HTTP_200_OK,
        summary="Stop Container",
        description="Stop a running container."
    )
    async def stop_container(vmid: int, container_service: Annotated[ContainerService, Depends(get_container_service)]) -> None:
        return await container_service.stop_container(vmid)

    @router.post(
        '/container/start',
        status_code=status.HTTP_200_OK,
        summary="Stop Container",
        description="Stop a running container."
    )
    async def start_container(vmid: int, container_service: Annotated[ContainerService, Depends(get_container_service)]) -> None:
        return await container_service.start_container(vmid)

    @router.post(
        '/container/restart',
        status_code=status.HTTP_200_OK,
        summary="Restart Container",
        description="Restart a specific container."
    )
    async def restart_container(vmid: int, container_service: Annotated[ContainerService, Depends(get_container_service)]) -> None:
        return await container_service.restart_container(vmid)

    @router.post(
        '/container/delete',
        status_code=status.HTTP_200_OK,
        summary="Delete Container",
        description="Delete an existing container by its identifier."
    )
    async def delete_container(vmid: int, container_service: Annotated[ContainerService, Depends(get_container_service)]) -> None:
        return await container_service.delete_container(vmid)

    @router.post(
        '/container/{id:str}',
        status_code=status.HTTP_201_CREATED,
        summary="Create New Container by UUID ticket",
        description="Create a new container and return a ticket for tracking."
    )
    async def create_container_by_ticket(id: UUID, container_service: Annotated[ContainerService, Depends(get_container_service)]) -> ContainerInfo:
        return await container_service.create_container_by_ticket(id)

    @router.get(
        '/container/telemetry/{vmid:int}',
        status_code=status.HTTP_200_OK,
        summary="Get Container Telemetry",
        description="Retrieve telemetry data and status for a specific container."
    )
    async def get_container_telemetry(vmid: int, container_service: Annotated[ContainerService, Depends(get_container_service)]) -> ContainerTelemetry | None:
        return await container_service.get_telemetry_container(vmid)

    @router.get(
        '/container/all',
        status_code=status.HTTP_200_OK,
        summary='Info all containers',
        description='Only for admins.'
    )
    async def all_info_contaners(container_service: Annotated[ContainerService, Depends(get_container_service)]) -> list[ContainerAdminInfo]:
        return await container_service.get_all_info_containers()

    '''@router.get(
        '/node/info',
        status_code=status.HTTP_200_OK,
        summary='Node info',
        description='Only for admins.'
    )
    async def node_info(container_service: Annotated[ContainerService, Depends(get_container_service)]):
        return await container_service.get_info_node()'''

    return router
