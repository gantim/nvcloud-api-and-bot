from typing import Any, Dict, Optional

import aiohttp

from app.config.proxmox import ProxmoxSettings


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
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        await self._ensure_session()
        async with self._session.request( # type: ignore
            method=method,
            url=endpoint,
            params=params,
            json=json
        ) as response:
            response.raise_for_status()
            return await response.json() # type: ignore

    async def create_network_bridge(self, node: str, bridge_name: str = "vmbr0") -> Dict[str, Any]:
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
        vmid: int,
        ostemplate: str,
        storage: str = "local-lvm",
        password: str = "fsggsfdgjlas",
        unprivileged: bool = True,
        start: bool = True,
        network_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Создает контейнер с автоматической настройкой сети

        :param network_config: {
            "bridge": "vmbr0",
            "ip": "192.168.100.100/24",
            "gw": "192.168.100.1",
            "dhcp": False  # Если True - ip/gw игнорируются
        }
        """
        if network_config is None:
            network_config = {
                "bridge": "vmbr0",
                "dhcp": True
            }

        net0 = f"name=eth0,bridge={network_config['bridge']}"
        if network_config.get("dhcp", True):
            net0 += ",ip=dhcp"
        else:
            net0 += f",ip={network_config['ip']},gw={network_config['gw']}"

        config = {
            "vmid": vmid,
            "ostemplate": ostemplate,
            "storage": storage,
            "password": password,
            "unprivileged": 1 if unprivileged else 0,
            "start": 1 if start else 0,
            "net0": net0,
            "features": "nesting=1",  # Для работы Docker внутри
            "memory": 1024,
            "cores": 1,
            "rootfs": f"{storage}:8",  # 8GB диска
        }

        '''# Сначала проверяем существование bridge
        try:
            await self._request(
                "GET",
                f"/api2/json/nodes/{node}/network/{network_config['bridge']}"
            )
        except aiohttp.ClientError:
            await self.create_network_bridge(node, network_config["bridge"])'''

        return await self._request(
            "POST",
            f"/api2/json/nodes/{node}/lxc",
            json=config
        )

    async def configure_container_network(
        self,
        node: str,
        vmid: int,
        network_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Обновляет сетевые настройки контейнера"""
        net0 = f"name=eth0,bridge={network_config['bridge']}"
        if network_config.get("dhcp", True):
            net0 += ",ip=dhcp"
        else:
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
    ) -> Dict[str, Any]:
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

    async def get_container_info(self, node: str, vmid: int) -> Dict[str, Any]:
        return await self._request(
            "GET",
            f"/api2/json/nodes/{node}/lxc/{vmid}/status/current"
        )

    async def delete_container(self, node: str, vmid: int) -> None:
        await self._request(
            "DELETE",
            f"/api2/json/nodes/{node}/lxc/{vmid}"
        )

    async def container_action(self, node: str, vmid: int, action: str) -> Dict[str, Any]:
        return await self._request(
            "POST",
            f"/api2/json/nodes/{node}/lxc/{vmid}/status/{action}"
        )
