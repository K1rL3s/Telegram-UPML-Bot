import datetime as dt

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, column_property, mapped_column

from shared.database.base import AlchemyBaseModel


class ClassLessons(AlchemyBaseModel):
    """Модель для хранения расписания уроков для конкретного класса."""

    __tablename__ = "class_lessons"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False,
    )

    date: Mapped[dt.date] = mapped_column(Date, nullable=False)
    grade: Mapped[str] = mapped_column(String(2), nullable=False)  # 10 или 11
    letter: Mapped[str] = mapped_column(String(1), nullable=False)  # А, Б, В
    class_: Mapped[str] = column_property(grade + letter)
    file_id: Mapped[str] = mapped_column(String(128), nullable=False)
