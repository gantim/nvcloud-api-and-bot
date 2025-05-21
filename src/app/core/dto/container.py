from dataclasses import dataclass
from typing import Literal


@dataclass
class CreatedContainer:
    node: str
    vmid: int
    hostname: str
    username: str
    password: str

    cpu_cores: int
    rom_bytes: int
    ram_bytes: int



@dataclass
class HAInfo:
    managed: int

@dataclass
class CurrentContainerInfo:
    status: Literal['stopped', 'running']
    maxdisk: int
    diskread: int
    type: str
    maxswap: int
    ha: HAInfo
    cpus: int
    swap: int
    uptime: int
    cpu: float
    disk: int
    netout: int
    mem: int
    maxmem: int
    netin: int
    diskwrite: int
    name: str
    vmid: int
    lock: bool | None = None
    pid: int | None = None
