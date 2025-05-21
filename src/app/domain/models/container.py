from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from .base import BaseEntity


class ContainerInDB(BaseEntity):
    id: UUID | None = None
    proxmox_vmid: int = 0
    proxmox_node: str
    name: str
    password: str
    owner_id: UUID | None
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    lxc_config: Optional[dict[str, Any]] = None
    is_template: bool = False
    is_protected: bool = False
    last_modified: Optional[datetime] = None
    owner_username: Optional[str] = None

