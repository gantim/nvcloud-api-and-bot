from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class NodeInfo(BaseModel):
    name: str = Field(..., description='Name node')
    rom_bytes: str = Field(..., description='Total rom in bytes')
    ram_bytes: str = Field(..., description='Total ram in bytes')
    cpu_load: int = Field(..., description='CPU load')

class CreateTicket(BaseModel):
    id: UUID = Field(..., description="Ticket ID")

class ContainerAdminInfo(BaseModel):
    id: int = Field(..., description="Container VMID")
    name: str = Field(..., description="Container host name")
    owner_username: str = Field(..., description="Username owner this is container")
    rom_bytes: int = Field(..., description="Rom in bytes")
    ram_bytes: int = Field(..., description="Ram in bytes")
    cpu_cores: int = Field(..., description="CPU cores")
    status: Literal['stopped', 'running', 'deleted'] = Field(..., description="Status Container")


class ContainerInfo(BaseModel):
    id: int = Field(..., description="Container VMID")
    name: str = Field(..., description="Container host name")
    status: Literal['stopped', 'running'] = Field(..., description="Status Container")


class CpuInfo(BaseModel):
    cpu_cores: int = Field(..., description="Number of CPU cores")
    free_cpu: float = Field(..., description="Available CPU percentage")


class RomInfo(BaseModel):
    rom_bytes: int = Field(..., description="Total ROM size in bytes")
    free_rom_bytes: int = Field(..., description="Free ROM size in bytes")


class RamInfo(BaseModel):
    ram_bytes: int = Field(..., description="Total RAM size in bytes")
    free_ram_bytes: int = Field(..., description="Free RAM size in bytes")


class UserPrivacyInfo(BaseModel):
    username: str = Field(..., description="Username for container access")
    password: str = Field(..., description="Password for container access")


class IoInfo(BaseModel):
    io_operations: int = Field(..., description="Number of disk input/output operations")


class NetworkTrafficInfo(BaseModel):
    incoming_total_bytes: int = Field(..., description="Total incoming network traffic in bytes")
    outgoing_total_bytes: int = Field(..., description="Total outgoing network traffic in bytes")
    incoming_current_bytes: int = Field(..., description="Current incoming network traffic in bytes")
    outgoing_current_bytes: int = Field(..., description="Current outgoing network traffic in bytes")


class ContainerTelemetry(BaseModel):
    container: ContainerInfo = Field(..., description="Container details")
    user: UserPrivacyInfo = Field(..., description="User credentials for the container")
    cpu: CpuInfo = Field(..., description="CPU usage information")
    ram: RamInfo = Field(..., description="RAM usage information")
    rom: RomInfo = Field(..., description="ROM usage information")
    io: IoInfo = Field(..., description="Disk input/output activity")
    network: NetworkTrafficInfo = Field(..., description="Network traffic information")
