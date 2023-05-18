from typing import List

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import Mapped, relationship

from src.database.models.base_model import BaseModel
from src.database.models.roles import Role
from src.database.models.users_to_roles import users_to_roles
from src.utils.datehelp import datetime_now


class User(BaseModel):
    __tablename__ = 'users'

    id = Column(
        Integer,
        primary_key=True, autoincrement=True,
        unique=True, nullable=False
    )
    user_id = Column(
        Integer,
        unique=True, nullable=False, index=True
    )

    # ТГ Никнейм пользователя
    username = Column(String(32), default=None)

    # Активный ли, False - заблокировал бота итп
    is_active = Column(Boolean, default=True, nullable=False)

    # Первый заход в бота
    createad_time = Column(
        DateTime,
        default=datetime_now, nullable=False
    )
    # Обновление ника или статуса
    modified_time = Column(
        DateTime,
        default=datetime_now,
        onupdate=datetime_now, nullable=False,
    )

    # Роли пользователя
    roles: Mapped[List[Role]] = relationship(secondary=users_to_roles)
    # Настройки пользователя
    settings = relationship('Settings', back_populates='user', lazy='selectin')
    # Таймер прачечной
    laundry = relationship('Laundry', back_populates='user', lazy='selectin')

    def short_info(self) -> str:
        return f'User(id={self.id}, user_id={self.user_id}, ' \
               f'username={self.username})'
