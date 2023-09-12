from sqlalchemy import Column, ForeignKey, Table

from bot.database import SqlAlchemyBase


# Подумать над записью таблицы через класс
users_to_roles = Table(
    "users_to_roles",
    SqlAlchemyBase.metadata,
    Column("user_id", ForeignKey("users.user_id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)
