import datetime as dt

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from bot.database.models.base_models import BaseModel


class EducatorsSchedule(BaseModel):
    """Модель для хранения расписания воспитателей на определённую дату."""

    __tablename__ = "educators_schedules"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False,
    )

    date: Mapped[dt.date] = mapped_column(
        Date,
        unique=True,
        nullable=False,
        index=True,
    )

    edit_by: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        default=0,
        nullable=False,
    )

    schedule: Mapped[str] = mapped_column(String(1024), nullable=True)
