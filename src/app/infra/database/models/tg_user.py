from typing import Any, Optional

from sqlalchemy import BigInteger, Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from .base import Base
from .mixins import SoftDeleteMixin


class TgUser(Base, SoftDeleteMixin):
    chat_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(
        String(50),
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

    user_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), unique=True, nullable=True)
    user: Mapped[Optional["User"]] = relationship("User", back_populates="tg_user")

from .user import User  # noqa: E402
