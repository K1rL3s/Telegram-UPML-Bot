import datetime as dt

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from shared.database.base import AlchemyBaseModel


class EducatorsSchedule(AlchemyBaseModel):
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
    edit_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=True,
    )
    schedule: Mapped[str] = mapped_column(String(1024), nullable=True)
