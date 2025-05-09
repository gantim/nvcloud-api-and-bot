from datetime import datetime
from uuid import UUID

from pydantic import BaseModel as PydanticBaseModel


class BaseEntity(PydanticBaseModel):
    id: UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
