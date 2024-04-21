from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from shared.database.base import AlchemyBaseModel


class UsersToRoles(AlchemyBaseModel):
    """Модель M2M связи пользователей и ролей доступа."""

    __tablename__ = "users_to_roles"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)
