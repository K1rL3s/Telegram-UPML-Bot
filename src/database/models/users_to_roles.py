from sqlalchemy import Column, ForeignKey, Table

from src.database.db_session import SqlAlchemyBase
# from src.database.models.base_model import BaseModel


# Подумать над записью таблицы через класс
users_to_roles = Table(
    'users_to_roles',
    SqlAlchemyBase.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)

# class UsersToRoles(BaseModel):
#     __tablename__ = 'users_to_roles'
#
#     user_id = Column(
#         Integer, ForeignKey('users.id'),
#         nullable=False, primary_key=True
#     )
#     role_id = Column(
#         Integer, ForeignKey('roles.id'),
#         nullable=False, primary_key=True
#     )
#
#     def __repr__(self):
#         return self._repr(
#             user_id=self.user_id,
#             role_id=self.role_id
#         )
