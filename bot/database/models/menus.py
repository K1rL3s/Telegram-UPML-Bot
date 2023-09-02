import datetime as dt

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from bot.database.models.base_models import BaseModel


class Menu(BaseModel):
    """Модель для хранения расписания еды на определённую дату."""

    __tablename__ = "menus"

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
        nullable=True,
    )

    breakfast: Mapped[str] = mapped_column(String, nullable=True)
    lunch: Mapped[str] = mapped_column(String, nullable=True)
    dinner: Mapped[str] = mapped_column(String, nullable=True)
    snack: Mapped[str] = mapped_column(String, nullable=True)
    supper: Mapped[str] = mapped_column(String, nullable=True)
