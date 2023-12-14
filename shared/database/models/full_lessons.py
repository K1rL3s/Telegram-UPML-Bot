import datetime as dt

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from shared.database.base import AlchemyBaseModel


class FullLessons(AlchemyBaseModel):
    """Модель для хранения расписания уроков для конкретной параллели."""

    __tablename__ = "full_lessons"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False,
    )

    date: Mapped[dt.date] = mapped_column(Date, nullable=False)
    grade: Mapped[str] = mapped_column(String(2), nullable=False)  # 10 или 11
    file_id: Mapped[str] = mapped_column(String(128), nullable=False)
