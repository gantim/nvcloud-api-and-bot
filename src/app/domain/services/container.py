from asyncio import gather
from typing import Any, AsyncContextManager
from uuid import UUID

from app.domain.models.container import ContainerInDB
from app.domain.models.ticket_container import TicketContainerInDB
from app.domain.models.user import UserInDB
from app.domain.providers.container import ContainerAPIProvider
from app.domain.schemas.container.request import CreateContainer
from app.domain.schemas.container.response import (
    ContainerAdminInfo,
    ContainerInfo,
    ContainerTelemetry,
    CpuInfo,
    CreateTicket,
    IoInfo,
    NetworkTrafficInfo,
    RamInfo,
    RomInfo,
    UserPrivacyInfo,
)
from app.domain.uow.abstract import AbstractUnitOfWork
from app.presentation.exceptions.auth import NoPermissions
from app.presentation.exceptions.container import (
    ContainerNotFound,
    TicketContainerClosed,
)


class ContainerService:
    def __init__(self, uow: AbstractUnitOfWork, container_provider: AsyncContextManager[ContainerAPIProvider], user: UserInDB):
        self._uow = uow
        self._container_provider = container_provider
        self._node = 'nvcloud'
        self._user = user

        self._is_template = [100]

    '''async def get_info_node(self) -> NodeInfo:
        if not self._user.is_superuser:
            raise NoPermissions

        async with self._container_provider as container_provider:
            raw_info_node = await container_provider.get_info_node(self._node)
        print(raw_info_node)'''

    async def check_permissions(self, vmid: int) -> ContainerInDB:
        async with self._uow:
            container = await self._uow.container_repo.get_by_vmid(vmid)

        if not container:
            raise ContainerNotFound

        if container.owner_id != self._user.id and not self._user.is_superuser: # type: ignore
            raise NoPermissions

        return container

    async def delete_container(self, vmid: int):
        await self.check_permissions(vmid)

        async with self._container_provider as container_provider:
            await container_provider.delete_container(self._node, vmid)
        async with self._uow:
            await self._uow.container_repo.delete_by_vmid(vmid)

        return True

    async def restart_container(self, vmid: int):
        await self.check_permissions(vmid)

        async with self._container_provider as container_provider:
            info_restarted = await container_provider.restart_container(self._node, vmid)
        print(info_restarted)

    async def stop_container(self, vmid: int):
        await self.check_permissions(vmid)

        async with self._container_provider as container_provider:
            info_restarted = await container_provider.stop_container(self._node, vmid)
        print(info_restarted)

    async def start_container(self, vmid: int):
        await self.check_permissions(vmid)

        async with self._container_provider as container_provider:
            info_restarted = await container_provider.start_container(self._node, vmid)
        print(info_restarted)


    async def get_all_info_containers(self) -> list[ContainerAdminInfo]:
        if not self._user.is_superuser:
            raise NoPermissions

        async with self._uow:
            _containers = await self._uow.container_repo.search()
        async with self._container_provider as container_provider:
            info_containers = await container_provider.get_info_all_containers(self._node)

        containers = {container.proxmox_vmid: container for container in _containers}
        info_containers = {info_container['vmid']: info_container for info_container in info_containers['data'] if 'vmid' in info_container} # type: ignore

        all_info_containers = [
            ContainerAdminInfo(
                id=int(vmid),
                name=info_vmid.get('name', 'Undefined'),
                owner_username=containers.get(vmid).owner_username if vmid in containers else 'Undefined', # type: ignore
                rom_bytes=info_vmid.get('maxdisk'),
                ram_bytes=info_vmid.get('maxmem'),
                cpu_cores=info_vmid.get('cpus'),
                status=info_vmid.get('status', 'stopped'),
            )
            for vmid, info_vmid in info_containers.items()
            if vmid not in self._is_template
        ]

        for vmid, container in containers.items():
            if vmid not in info_containers and vmid not in self._is_template:
                all_info_containers.append(ContainerAdminInfo(
                id=int(vmid), # type: ignore
                name=container.name,
                owner_username=container.owner_username, # type: ignore
                rom_bytes=container.lxc_config.get('rom_bytes', 0), # type: ignore
                ram_bytes=container.lxc_config.get('ram_bytes', 0), # type: ignore
                cpu_cores=container.lxc_config.get('cpu_cores', 0), # type: ignore
                status='stopped',
            ))


        return all_info_containers

    async def get_tickets_container(self) -> list[TicketContainerInDB]:
        if not self._user.is_superuser:
            raise NoPermissions
        async with self._uow:
            tickets_container = await self._uow.ticket_container_repo.search()
        return tickets_container

    async def delete_ticket_container(self, id: UUID):
        if self._user.is_superuser:
            async with self._uow:
                await self._uow.ticket_container_repo.delete(id)

    async def create_ticket_container(self, create_container: CreateContainer) -> CreateTicket:
        ticket_container = TicketContainerInDB(
            name=create_container.host_name,
            ram_bytes=create_container.ram_bytes,
            rom_bytes=create_container.rom_bytes,
            cpu_cores=create_container.cpu_cores,
            owner_id=self._user.id
        )
        async with self._uow:
            ticket_container = await self._uow.ticket_container_repo.add(ticket_container)

        return CreateTicket(id=ticket_container.id) # type: ignore

    async def get_telemetry_container(self, vmid: int) -> ContainerTelemetry | None:
        container = await self.check_permissions(vmid)

        async with self._container_provider as container_provider:
            container_telemetries = await container_provider.get_container_telemetry(container.proxmox_node, container.proxmox_vmid) # type: ignore

            container_info = await container_provider.get_container_info(container.proxmox_node, container.proxmox_vmid) # type: ignore

            container_telemetry: dict[str, Any] = next(
                (item for item in reversed(container_telemetries['data']) if 'cpu' in item),
                None # type: ignore
            )

        status = container_info.status

        status_stop = status == 'stopped'

        if not container_telemetry:
            container_telemetry = {}

        if status_stop:
            con_tel = ContainerTelemetry(
                container=ContainerInfo(id=container.proxmox_vmid, name=container_info.name, status=container_info.status), # type: ignore
                user=UserPrivacyInfo(username='root', password=container.password), # type: ignore
                cpu=CpuInfo(cpu_cores=container_info.cpus, free_cpu=1),
                ram=RamInfo(ram_bytes=int(container_telemetry.get('maxmem', 0)), free_ram_bytes=int(container_telemetry.get('maxmem', 0))),
                rom=RomInfo(rom_bytes=int(container_telemetry.get('maxdisk', 0)), free_rom_bytes=int(container_telemetry.get('maxdisk', 0))),
                io=IoInfo(io_operations=0),
                network=NetworkTrafficInfo(
                    incoming_total_bytes=int(container_info.netin),
                    outgoing_total_bytes=int(container_info.netout),
                    incoming_current_bytes=0,
                    outgoing_current_bytes=0
                    )
                )
        else:
            con_tel = ContainerTelemetry(
                container=ContainerInfo(id=container.proxmox_vmid, name=container_info.name, status=container_info.status), # type: ignore
                user=UserPrivacyInfo(username='root', password=container.password), # type: ignore
                cpu=CpuInfo(cpu_cores=container_info.cpus, free_cpu=1-container_info.cpu),
                ram=RamInfo(ram_bytes=int(container_telemetry.get('maxmem', 0)), free_ram_bytes=int(container_telemetry.get('maxmem', 0) - container_telemetry.get('mem', 0))),
                rom=RomInfo(rom_bytes=int(container_telemetry.get('maxdisk', 0)), free_rom_bytes=int(container_telemetry.get('maxdisk', 0) - container_telemetry.get('disk', 0))),
                io=IoInfo(io_operations=int(container_telemetry.get('diskread', 0) + container_telemetry.get('diskwrite', 0))),
                network=NetworkTrafficInfo(
                    incoming_total_bytes=int(container_info.netin),
                    outgoing_total_bytes=int(container_info.netout),
                    incoming_current_bytes=int(container_telemetry.get('netin', 0)),
                    outgoing_current_bytes=int(container_telemetry.get('netout', 0))
                )
            )

        return con_tel

    async def get_containers(self) -> list[ContainerInfo]:
        async with self._uow:
            containers = await self._uow.container_repo.search(owner_id=self._user.id)

        async with self._container_provider as container_provider:
            containers_telemetry = await gather(*[
                container_provider.get_container_info(container.proxmox_node, container.proxmox_vmid)
                for container in containers
            ])

        containers_info = [
            ContainerInfo(
                id=container.proxmox_vmid, name=container.name, status=container_telemetry.status
            )
            for container, container_telemetry in zip(containers, containers_telemetry, strict=True)
        ]

        return containers_info

    async def create_container(self, create_container: CreateContainer) -> ContainerInfo:
        async with self._container_provider as container_provider:
            created_container = await container_provider.create_container(
                node=self._node,
                host_name=create_container.host_name,
                ram_bytes=create_container.ram_bytes,
                rom_bytes=create_container.rom_bytes,
                cpu_cores=create_container.cpu_cores
            )

        container = ContainerInDB(
            proxmox_node=created_container.node,
            proxmox_vmid=created_container.vmid,
            name=created_container.hostname,
            password=created_container.password,
            lxc_config={
                'cpu_cores': created_container.cpu_cores,
                'rom_bytes': created_container.rom_bytes,
                'ram_bytes': created_container.ram_bytes
            },
            owner_id=self._user.id,
            owner_username=self._user.username
        )

        async with self._uow:
            await self._uow.container_repo.add(container)

        container_telemetry = await container_provider.get_container_info(container.proxmox_node, container.proxmox_vmid)

        return ContainerInfo(
            id=container.proxmox_vmid,
            name=container.name,
            status=container_telemetry.status
        )

    async def create_container_by_ticket(self, id: UUID) -> ContainerInfo:
        async with self._uow:
            ticket_container = await self._uow.ticket_container_repo.get(id)
            if ticket_container:
                if ticket_container.closed:
                    raise TicketContainerClosed
                ticket_container.closed = True
                async with self._container_provider as container_provider:
                    created_container = await container_provider.create_container(
                        node=self._node,
                        host_name=ticket_container.name,
                        ram_bytes=ticket_container.ram_bytes,
                        rom_bytes=ticket_container.rom_bytes,
                        cpu_cores=ticket_container.cpu_cores
                    )

                container = ContainerInDB(
                    proxmox_node=created_container.node,
                    proxmox_vmid=created_container.vmid,
                    name=created_container.hostname,
                    password=created_container.password,
                    lxc_config={
                        'cpu_cores': created_container.cpu_cores,
                        'rom_bytes': created_container.rom_bytes,
                        'ram_bytes': created_container.ram_bytes
                    },
                    owner_id=ticket_container.owner_id,
                    owner_username=ticket_container.owner_username
                )

                await self._uow.container_repo.add(container)
                await self._uow.ticket_container_repo.update(ticket_container)

                container_telemetry = await container_provider.get_container_info(container.proxmox_node, container.proxmox_vmid)

        return ContainerInfo(
            id=container.proxmox_vmid,
            name=container.name,
            status=container_telemetry.status
        )
