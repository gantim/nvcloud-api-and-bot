from typing import Any, Optional

import aiohttp

from app.config.proxmox import ProxmoxSettings
from app.core.dto.container import CreatedContainer, CurrentContainerInfo, HAInfo
from app.core.security.password import generate_password


class ProxmoxProvider:
    def __init__(self, settings: ProxmoxSettings):
        self.settings = settings
        self._session: Optional[aiohttp.ClientSession] = None

    async def _ensure_session(self) -> None:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                base_url=self.settings.BASE_URL,
                headers={
                    "Authorization": f"PVEAPIToken={self.settings.API_TOKEN_ID}={self.settings.API_TOKEN_SECRET}"
                },
                connector=aiohttp.TCPConnector(ssl=self.settings.VERIFY_SSL),
                timeout=aiohttp.ClientTimeout(total=self.settings.TIMEOUT)
            )

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        await self._ensure_session()
        async with self._session.request( # type: ignore
            method=method,
            url=endpoint,
            params=params,
            json=json
        ) as response:
            response.raise_for_status()
            return await response.json() # type: ignore

    async def create_network_bridge(self, node: str, bridge_name: str = "vmbr0") -> dict[str, Any]:
        """Создает bridge-интерфейс если не существует"""
        return await self._request(
            "POST",
            f"/api2/json/nodes/{node}/network",
            json={
                "iface": bridge_name,
                "type": "bridge",
                "autostart": 1
            }
        )

    async def create_container(
        self,
        node: str,
        host_name: str,
        storage: str = "local-lvm",
        ostemplate: str = "local:vztmpl/vzdump-lxc-100-2025_05_13-17_31_15.tar.zst",
        ram_bytes: int = 1_024 ** 3,  # 1GB в байтах
        rom_bytes: int = 5 * 1_024 ** 3,  # 5GB в байтах
        cpu_cores: int = 1,
        unprivileged: bool = True,
        start: bool = True,
        network_config: Optional[dict[str, Any]] = None
    ) -> CreatedContainer:
        """
        Создает контейнер с автоматической настройкой сети и генерацией пароля

        :param network_config: {
            "bridge": "vmbr0",
            "ip": "192.168.100.100/24",
            "gw": "192.168.100.1",
            "dhcp": False  # Если True - ip/gw игнорируются
        }
        :param ram_bytes: ОЗУ в байтах (будет переведено в МБ для API)
        :param rom_bytes: Диск в байтах (будет переведено в ГБ для API)
        """
        vmids = await self.get_container_vmids('nvcloud')

        vmid = 100
        while vmid in vmids:
            vmid += 1

        if vmid > 199:
            raise Exception(f'Max vmid: {vmid}')

        if network_config is None:
            network_config = {"bridge": "vmbr0", 'gw': '192.168.1.1'}


        net0 = f"name=eth0,bridge={network_config['bridge']}"
        net0 += f",ip=192.168.1.{vmid}/24,gw={network_config['gw']}"

        random_password = generate_password(12, use_special_chars=False)

        ram_mb = ram_bytes // (1024 * 1024)  # Байты -> Мегабайты
        rootfs_gb = rom_bytes // (1024 * 1024 * 1024)  # Байты -> Гигабайты

        config = {
            "vmid": vmid,
            "ostemplate": ostemplate,
            "storage": storage,
            "unprivileged": 1 if unprivileged else 0,
            "password": random_password,
            "hostname": host_name,
            "onboot": 1,
            "start": 1 if start else 0,
            "net0": net0,
            "features": "nesting=1",
            "memory": ram_mb,  # Указывается в МБ
            "cores": cpu_cores,
            "rootfs": f"{storage}:{rootfs_gb}",  # Указывается в ГБ
        }

        try:
            await self._request(
                "POST",
                f"/api2/json/nodes/{node}/lxc",
                json=config
            )

            return CreatedContainer(
                node=node,
                vmid=vmid,
                hostname=host_name,
                username='root',
                password=random_password,
                cpu_cores=cpu_cores,
                rom_bytes=rom_bytes,
                ram_bytes=ram_bytes
            )

        except Exception as e:
            raise Exception(f'Error creating container: {e} {e.args}') from e

    async def configure_container_network(
        self,
        node: str,
        vmid: int,
        network_config: dict[str, Any]
    ) -> dict[str, Any]:
        """Обновляет сетевые настройки контейнера"""
        net0 = f"name=eth0,bridge={network_config['bridge']}"
        net0 += f",ip={network_config['ip']},gw={network_config['gw']}"

        return await self._request(
            "PUT",
            f"/api2/json/nodes/{node}/lxc/{vmid}/config",
            json={"net0": net0}
        )

    async def enable_internet_access(
        self,
        node: str,
        vmid: int,
        public_ip: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Настраивает NAT для доступа в интернет
        :param public_ip: Если None - используется NAT через хост
        """
        if public_ip:
            # Назначаем публичный IP напрямую контейнеру
            return await self.configure_container_network(
                node,
                vmid,
                {
                    "bridge": "vmbr0",
                    "ip": f"{public_ip}/24",
                    "gw": "95.123.123.1",  # Пример GW
                    "dhcp": False
                }
            )
        else:
            # Настраиваем NAT через iptables API Proxmox
            return await self._request(
                "POST",
                f"/api2/json/nodes/{node}/firewall/rules",
                json={
                    "enable": 1,
                    "type": "in",
                    "action": "ACCEPT",
                    "source": f"CT_{vmid}",
                    "dest": "internet"
                }
            )

    async def get_container_info(self, node: str, vmid: int) -> CurrentContainerInfo:
        raw: dict[str, Any] = await self._request( # type: ignore
            "GET",
            f"/api2/json/nodes/{node}/lxc/{vmid}/status/current"
        )

        container_info = CurrentContainerInfo(
            **{
                **raw['data'],
                'ha': HAInfo(**raw['data']['ha'])
            }
        )

        return container_info

    async def get_container_telemetry(self, node: str, vmid: int, timeframe: str = 'hour') -> dict[str, Any]:
        return await self._request(
            "GET",
            f"/api2/json/nodes/{node}/lxc/{vmid}/rrddata?timeframe={timeframe}&cf=AVERAGE"
        )

    async def delete_container(self, node: str, vmid: int) -> dict[str, Any]:
        return await self._request(
            "DELETE",
            f"/api2/json/nodes/{node}/lxc/{vmid}"
        )

    async def restart_container(self, node: str, vmid: int) -> dict[str, Any]:
        return await self._request(
            "POST",
            f"/api2/json/nodes/{node}/lxc/{vmid}/status/reboot"
        )

    async def start_container(self, node: str, vmid: int) -> dict[str, Any]:
        return await self._request(
            "POST",
            f"/api2/json/nodes/{node}/lxc/{vmid}/status/start"
        )

    async def stop_container(self, node: str, vmid: int) -> dict[str, Any]:
        return await self._request(
            "POST",
            f"/api2/json/nodes/{node}/lxc/{vmid}/status/stop"
        )

    async def get_info_all_containers(self, node: str) -> dict[str, Any]:
        return await self._request(
            "GET",
            f"/api2/json/nodes/{node}/lxc"
        )

    async def get_info_node(self, node: str) -> dict[str, Any]:
        return await self._request(
            "GET",
            f"/api2/json/nodes/{node}/status"
        )

    async def container_action(self, node: str, vmid: int, action: str) -> dict[str, Any]:
        return await self._request(
            "POST",
            f"/api2/json/nodes/{node}/lxc/{vmid}/status/{action}"
        )

    async def get_container_vmids(self, node: str) -> list[int]:
        data: dict[str, Any] = await self._request(
            "GET",
            f"/api2/json/nodes/{node}/lxc/"
        )
        vmids = [vm.get('vmid') for vm in data['data']]

        return vmids
