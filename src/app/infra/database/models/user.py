from typing import Any, Optional

from sqlalchemy import Boolean, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from .base import Base
from .mixins import SoftDeleteMixin


class User(Base, SoftDeleteMixin):
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )
    hashed_password: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=expression.false(),
        nullable=False
    )

    full_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    meta: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSONB,
        nullable=True,
        server_default='{}'
    )

    containers: Mapped[list["Container"]] = relationship("Container", back_populates="owner", lazy='selectin')
    ticketcontainers: Mapped[list["TicketContainer"]] = relationship("TicketContainer", back_populates="owner", lazy='selectin')
    tg_user: Mapped[Optional["TgUser"]] = relationship("TgUser", back_populates="user", uselist=False, lazy='selectin')

from .container import Container  # noqa: E402
from .tg_user import TgUser  # noqa: E402
from .ticket_container import TicketContainer  # noqa: E402
