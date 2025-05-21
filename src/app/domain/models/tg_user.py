from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TgUserInDB(BaseModel):
    chat_id: int = Field( # type: ignore
        ...,
        gt=0,
        description="Telegram user ID (unique identifier)",
        example=123456789
    )
    user_id: UUID | None = Field( # type: ignore
        ...,
        description="User UUID",
    )

    username: str | None = Field( # type: ignore
        ...,
        description="Telegram username (without @)",
        example="johndoe",
        min_length=1,
        max_length=50
    )

    full_name: Optional[str] = Field( # type: ignore
        None,
        description="User's full name as set in Telegram",
        example="John Doe",
        max_length=100
    )

    meta: Dict[str, Any] = Field( # type: ignore
        default_factory=dict,
        description="Additional metadata about the user",
        example={"language": "en", "last_command": "/start"}
    )

    is_superuser: bool = Field(default=False)

    created_at: datetime | None = Field( # type: ignore
        None,
        description="When the user record was created",
        example="2023-01-01T00:00:00Z"
    )

    updated_at: datetime | None = Field( # type: ignore
        None,
        description="When the user record was last updated",
        example="2023-01-01T00:00:00Z"
    )

    is_deleted: bool | None = Field( # type: ignore
        False,
        description="Whether the user is soft-deleted",
        example=False
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "description": "Complete Telegram user information as stored in database"
        }
