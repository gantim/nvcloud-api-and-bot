from typing import Annotated

from pydantic import EmailStr, Field

from .base import BaseEntity


class UserInDB(BaseEntity):
    username: Annotated[
        str,
        Field(
            ...,
            min_length=3,
            max_length=50,
            pattern=r"^[a-zA-Z0-9_-]+$",
            examples=["john_doe123"],
            title="Username",
            description="3-50 characters, letters, numbers, underscores or hyphens"
        )
    ]
    email: EmailStr = Field(..., title="Email Address", description="The email address used for registration. It must be a valid email format.")
    full_name: str = Field(..., title='Full Name')
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    hashed_password: str = Field(..., example="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW") # type: ignore

    class Config:
        from_attributes = True
