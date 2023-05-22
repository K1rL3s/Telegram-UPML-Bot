from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.database.models.base_model import BaseModel


class Laundry(BaseModel):
    __tablename__ = 'laundries'

    id = Column(
        Integer,
        primary_key=True, autoincrement=True,
        unique=True, nullable=False
    )
    user_id = Column(
        Integer, ForeignKey('users.id'),
        unique=True, nullable=False
    )

    # Когда был запущен таймер
    start_time = Column(DateTime)
    # Когда он должен закончится
    end_time = Column(DateTime)
    # Сколько раз было уведомление
    rings = Column(Integer)
    # Активен ли таймер
    is_active = Column(Boolean)

    user = relationship('User', back_populates='laundry', lazy='selectin')
