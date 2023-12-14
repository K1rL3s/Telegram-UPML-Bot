from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.database.base import UserRelatedModel

if TYPE_CHECKING:
    from shared.database.models.laundries import Laundry
    from shared.database.models.roles import Role
    from shared.database.models.settings import Settings


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
    username: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    # Активный ли, False - заблокировал бота итп
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
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

    def should_be_updated(self, username: str) -> bool:
        """
        Нужно ли активировать пользователя или обновить ему имя.

        :param username: Имя пользователя в ТГ.
        :return: Нужно ли поставить новый никнейм или изменить статус на активный.
        """
        return not self.is_active or self.username != username
