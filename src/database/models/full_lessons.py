import datetime

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base_model import BaseModel


class FullLessons(BaseModel):
    __tablename__ = 'full_lessons'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True, autoincrement=True,
        unique=True, nullable=False,
    )

    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)

    grade: Mapped[str] = mapped_column(String(2), nullable=False)  # 10 или 11
    # Айди изображения из тг
    image: Mapped[str] = mapped_column(String, nullable=False)
