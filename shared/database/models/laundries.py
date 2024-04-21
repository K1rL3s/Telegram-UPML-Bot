import datetime as dt

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.database.base import UserRelatedModel


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

    # Когда таймер должен закончиться
    end_time: Mapped[dt.datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )
    # Сколько раз было уведомление
    rings: Mapped[int | None] = mapped_column(
        Integer,
        default=0,
        nullable=True,
    )
    # Активен ли таймер
    is_active: Mapped[bool | None] = mapped_column(
        Boolean,
        default=False,
        nullable=True,
    )

    user = relationship("User", back_populates="laundry", lazy="selectin")
