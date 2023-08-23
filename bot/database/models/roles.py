from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from bot.database.models.base_models import BaseModel


class Role(BaseModel):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False,
    )

    role: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
