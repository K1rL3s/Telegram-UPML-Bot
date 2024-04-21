from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from shared.database.base import AlchemyBaseModel


class Role(AlchemyBaseModel):
    """Модель, представляющая роль - уровень доступа пользователя."""

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False,
    )

    role: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
