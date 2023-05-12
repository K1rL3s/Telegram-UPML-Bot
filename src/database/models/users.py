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

    username = Column(String(32), default=None)
    grade = Column(Integer, default=None)  # 10 или 11
    letter = Column(String(1), default=None)  # Буква класса, русская

    lessons_notify = Column(Boolean, default=False, nullable=False)
    news_notify = Column(Boolean, default=False, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)
    roles: Mapped[List[Role]] = relationship(secondary=users_to_roles)

    createad_time = Column(
        DateTime,
        default=datetime_now, nullable=False
    )
    modified_time = Column(
        DateTime,
        default=datetime_now,
        onupdate=datetime_now, nullable=False,
    )

    def __repr__(self):
        return self._repr(
            id=self.id,
            user_id=self.user_id,
            grade=self.grade,
            letter=self.letter,
            lessons_notify=self.lessons_notify,
            news_notify=self.news_notify,
            is_active=self.is_active,
            roles=self.roles,
            createad_time=self.createad_time,
            modified_time=self.modified_time,
        )
