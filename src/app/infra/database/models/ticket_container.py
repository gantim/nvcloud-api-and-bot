from uuid import UUID

from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class TicketContainer(Base):
    proxmox_node: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    password: Mapped[str] = mapped_column(String, server_default="")

    closed: Mapped[bool] = mapped_column(Boolean, server_default="false", nullable=False)

    rom_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    ram_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    cpu_cores: Mapped[int] = mapped_column(Integer, nullable=False)

    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    owner: Mapped["User"] = relationship("User", back_populates="ticketcontainers", lazy='selectin')


from .user import User  # noqa: E402
