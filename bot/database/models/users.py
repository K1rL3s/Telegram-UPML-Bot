import datetime as dt

from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.database.base import UserRelatedModel
from bot.utils.datehelp import datetime_now

if TYPE_CHECKING:
    from bot.database.models.laundries import Laundry
    from bot.database.models.roles import Role
    from bot.database.models.settings import Settings


class User(UserRelatedModel):
    """Модель для хранения информации о пользователе."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
        index=True,
    )
    # ТГ Никнейм пользователя (64?)
    username: Mapped[str] = mapped_column(String(32), default=None)

    # Активный ли, False - заблокировал бота итп
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Первый заход в бота  UNUSED !!
    createad_time: Mapped[dt.datetime] = mapped_column(
        DateTime,
        default=datetime_now,
        nullable=False,
    )
    # Обновление ника или статуса  UNUSED !!
    modified_time: Mapped[dt.datetime] = mapped_column(
        DateTime,
        default=datetime_now,
        onupdate=datetime_now,
        nullable=False,
    )

    # Настройки пользователя
    settings: Mapped["Settings"] = relationship(
        "Settings",
        back_populates="user",
        lazy="selectin",
    )
    # Таймер прачечной
    laundry: Mapped["Laundry"] = relationship(
        "Laundry",
        back_populates="user",
        lazy="selectin",
    )
    # Роли пользователя
    roles: Mapped[list["Role"]] = relationship(
        secondary="users_to_roles",
        lazy="selectin",
    )

    @property
    def short_info(self) -> str:
        """Краткая информация о пользователе."""
        return f"User(id={self.id}, user_id={self.user_id}, username={self.username})"

    def should_activate(self, username: str) -> bool:
        """
        Нужно ли активировать пользователя или обновить ему имя.

        :param username: Имя пользователя в ТГ.
        :return: Нужно ли поставить новый никнейм или изменить статус на активный.
        """
        return not self.is_active or self.username != username
