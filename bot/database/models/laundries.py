import datetime as dt
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.database.base import UserRelatedModel


class Laundry(UserRelatedModel):
    """Модель для хранения таймера прачечной одного пользователя."""

    __tablename__ = "laundries"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        unique=True,
        nullable=False,
    )

    # Когда был запущен таймер  UNUSED !!
    start_time: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )
    # Когда он должен закончится
    end_time: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )
    # Сколько раз было уведомление
    rings: Mapped[Optional[int]] = mapped_column(
        Integer,
        default=0,
        nullable=True,
    )
    # Активен ли таймер
    is_active: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        default=False,
        nullable=True,
    )

    user = relationship("User", back_populates="laundry", lazy="selectin")
