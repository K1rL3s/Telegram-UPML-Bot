import datetime
from typing import List

from sqlalchemy import BigInteger, Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base_model import BaseModel
from src.database.models.laundries import Laundry
from src.database.models.roles import Role
from src.database.models.settings import Settings
from src.database.models.users_to_roles import users_to_roles
from src.utils.datehelp import datetime_now


class User(BaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True, autoincrement=True,
        unique=True, nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True, nullable=False, index=True,
    )

    # ТГ Никнейм пользователя
    username: Mapped[str] = mapped_column(String(32), default=None)

    # Активный ли, False - заблокировал бота итп
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True, nullable=False,
    )

    # Первый заход в бота
    createad_time: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime_now, nullable=False,
    )
    # Обновление ника или статуса
    modified_time: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime_now,
        onupdate=datetime_now, nullable=False,
    )

    # Роли пользователя
    roles: Mapped[List[Role]] = relationship(
        secondary=users_to_roles, lazy='selectin'
    )
    # Настройки пользователя
    settings: Mapped[Settings] = relationship(
        'Settings',
        back_populates='user', lazy='selectin',
    )
    # Таймер прачечной
    laundry: Mapped[Laundry] = relationship(
        'Laundry',
        back_populates='user', lazy='selectin',
    )

    def short_info(self) -> str:
        return f'User(id={self.id}, user_id={self.user_id}, ' \
               f'username={self.username})'
