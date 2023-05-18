from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import column_property, relationship

from src.database.models.base_model import BaseModel


class Settings(BaseModel):
    __tablename__ = 'settings'

    id = Column(
        Integer,
        primary_key=True, autoincrement=True,
        unique=True, nullable=False
    )
    user_id = Column(
        Integer, ForeignKey('users.id'),
        nullable=False, unique=True
    )

    # Класс, 10 или 11
    grade = Column(String(2), default=None)
    # Буква класса, русская
    letter = Column(String(1), default=None)
    # grade + letter, например, "10Б", "11А" итп
    class_ = column_property(grade + letter)

    # Включены ли уведомления об обновлении расписания
    lessons_notify = Column(Boolean, default=None, nullable=False)
    # Включены ли уведомления новостных сообщений
    news_notify = Column(Boolean, default=None, nullable=False)

    # Сколько времени стирается бельё
    washing_time = Column(Integer, default=60, nullable=False)
    # Сколько времени сушится бельё
    drying_time = Column(Integer, default=1440, nullable=False)

    user = relationship('User', back_populates='settings', lazy='selectin')
