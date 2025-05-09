from abc import ABC, abstractmethod
from typing import Any

from pydantic_settings import BaseSettings


class ContainerAPIProvider(ABC):
    @abstractmethod
    def __init__(self, settings: BaseSettings) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...

    @abstractmethod
    async def get_container_info(self, node: str, vmid: int) -> dict[str, Any]: ...

    @abstractmethod
    async def create_container(
        self,
        node: str,
        vmid: int,
        ostemplate: str,
        storage: str = "local-lvm",
        password: str = "securepassword",
        unprivileged: bool = False,
        start: bool = True,
        network_config: dict[str, Any] | None = None
        ) -> dict[str, Any]: ...

    @abstractmethod
    async def delete_container(self, node: str, vmid: int) -> dict[str, Any]: ...

    @abstractmethod
    async def get_container_telemetry(self, node: str, vmid: int) -> dict[str, Any]: ...

    @abstractmethod
    async def container_action(self, node: str, vmid: int, action: str) -> dict[str, Any]: ...

