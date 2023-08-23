import datetime

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from bot.database.models.base_models import BaseModel


class Menu(BaseModel):
    __tablename__ = "menus"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False,
    )

    date: Mapped[datetime.date] = mapped_column(
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

    breakfast: Mapped[str] = mapped_column(String, nullable=True)
    lunch: Mapped[str] = mapped_column(String, nullable=True)
    dinner: Mapped[str] = mapped_column(String, nullable=True)
    snack: Mapped[str] = mapped_column(String, nullable=True)
    supper: Mapped[str] = mapped_column(String, nullable=True)
