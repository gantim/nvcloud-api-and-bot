from pydantic import BaseModel, Field


class CreateContainer(BaseModel):
    host_name: str = Field(...)
    rom_bytes: int = Field(...)
    ram_bytes: int = Field(...)
    cpu_cores: int = Field(...)
