from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Container(Base):
    # Связь с Proxmox (обязательные поля)
    proxmox_vmid: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    proxmox_node: Mapped[str] = mapped_column(String(64), nullable=False)

    # Базовые метаданные (редко меняются)
    name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(512))
    tags: Mapped[list[str]] = mapped_column(JSONB, server_default="[]")

    # Конфигурация LXC (только важные статичные параметры)
    lxc_config: Mapped[dict[str, Any]] = mapped_column(JSONB, server_default="{}")

    # Владелец и проект
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    #project_id: Mapped[UUID] = mapped_column(ForeignKey("projects.id"))

    # Флаги
    is_template: Mapped[bool] = mapped_column(Boolean, default=False)
    is_protected: Mapped[bool] = mapped_column(Boolean, default=False)

    # Временные метки
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default="now()")
    last_modified: Mapped[datetime] = mapped_column(
        DateTime,
        server_default="now()",
        onupdate="now()"
    )

    # Связи
    owner: Mapped["User"] = relationship("User", back_populates="containers")
    #project: Mapped["Project"] = relationship(back_populates="containers")

    # Методы доступа
    def get_proxmox_url(self) -> str:
        return f"/nodes/{self.proxmox_node}/lxc/{self.proxmox_vmid}"


from .user import User  # noqa: E402
