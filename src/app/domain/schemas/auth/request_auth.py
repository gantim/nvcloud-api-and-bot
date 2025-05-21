from typing import Annotated, Any

from pydantic import BaseModel, EmailStr, Field, model_validator


class LogIn(BaseModel):
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
    password: Annotated[
        str,
        Field(
            ...,
            title="Password",
            description="The password for the user account. It should be at least 8 characters long.",
            min_length=8,
            max_length=24,
            pattern=r'^[A-Za-z\d!@#$%^&*()_+\-=\[\]{}|\\;:\'",.<>\/?]{8,}$'
        )
    ]


class SignUp(LogIn):
    email: Annotated[
        EmailStr,
        Field(
            ...,
            title="Email Address",
            description="The email address used to log in. It must be a valid email format."
        )
    ]
    full_name: Annotated[
        str,
        Field(
            ...,
            title="Full Name",
            description="The user's full name, which will be displayed on their profile. Please provide your first and last name."
        )
    ]

    @model_validator(mode="before")
    def check_full_name(cls, values: dict[str, Any]) -> dict[str, Any]:
        full_name = values.get("full_name", "")
        if len(full_name.split()) != 3:
            raise ValueError("Full name must consist of exactly three words.")
        return values
