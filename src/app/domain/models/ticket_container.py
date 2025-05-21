from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import Field

from .base import BaseEntity


class TicketContainerInDB(BaseEntity):
    id: UUID | None = None
    name: str
    owner_id: UUID | None
    closed: bool = False
    rom_bytes: int = Field(...)
    ram_bytes: int = Field(...)
    cpu_cores: int = Field(...)
    last_modified: Optional[datetime] = None
    owner_username: Optional[str] = None

