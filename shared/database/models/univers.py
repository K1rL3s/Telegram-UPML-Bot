from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from shared.database.base import AlchemyBaseModel


class Univer(AlchemyBaseModel):
    """Модель для хранения информации о вузах."""

    __tablename__ = "univers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(String(64), nullable=False)
    city: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[str] = mapped_column(String(512 * 7), nullable=False)
