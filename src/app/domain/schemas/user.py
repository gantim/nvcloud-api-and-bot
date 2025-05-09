from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserProfile(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    total_containers: int
    registration_date: datetime
