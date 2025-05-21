from abc import ABC, abstractmethod
from typing import Any

from pydantic_settings import BaseSettings

from app.core.dto.container import CreatedContainer, CurrentContainerInfo


class ContainerAPIProvider(ABC):
    @abstractmethod
    def __init__(self, settings: BaseSettings) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...

    @abstractmethod
    async def get_container_info(self, node: str, vmid: int) -> CurrentContainerInfo: ...

    @abstractmethod
    async def create_container(
        self,
        node: str,
        host_name: str,
        storage: str = "local-lvm",
        ostemplate: str = "local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst",
        ram_bytes: int = 1_048_576,  # 1GB в байтах
        rom_bytes: int = 5_242_880,  # 5GB в байтах
        cpu_cores: int = 1,
        unprivileged: bool = True,
        start: bool = True,
        network_config: dict[str, Any] | None = None
        ) -> CreatedContainer: ...

    @abstractmethod
    async def restart_container(self, node: str, vmid: int) -> dict[str, Any]: ...

    @abstractmethod
    async def start_container(self, node: str, vmid: int) -> dict[str, Any]: ...

    @abstractmethod
    async def stop_container(self, node: str, vmid: int) -> dict[str, Any]: ...

    @abstractmethod
    async def delete_container(self, node: str, vmid: int) -> dict[str, Any]: ...

    @abstractmethod
    async def get_container_telemetry(self, node: str, vmid: int) -> dict[str, Any]: ...

    @abstractmethod
    async def get_actual_container_info(self, node: str, vmid: int, timeframe: str = 'hour') -> dict[str, Any]: ...

    @abstractmethod
    async def container_action(self, node: str, vmid: int, action: str) -> dict[str, Any]: ...

    @abstractmethod
    async def get_container_vmids(self, node: str) -> dict[str, Any]: ...

    @abstractmethod
    async def get_info_all_containers(self, node: str) -> dict[str, Any]: ...

    @abstractmethod
    async def get_info_node(self, node: str) -> dict[str, Any]: ...

