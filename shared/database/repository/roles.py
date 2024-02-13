from enum import Enum
from typing import Optional, Union

from sqlalchemy import select

from shared.database.models.roles import Role
from shared.database.repository.base_repo import BaseRepository
from shared.utils.enums import RoleEnum


class RoleRepository(BaseRepository):
    """Класс для работы с ролями в базе данных."""

    async def get(
        self,
        role: "Union[RoleEnum | str]",
    ) -> "Optional[Role]":
        """
        Возвращает модель Role по названию роли.

        :param role: Название роли.
        :return: Модель Role.
        """
        if isinstance(role, Enum):
            role = role.value

        query = select(Role).where(Role.role == role)
        return await self._session.scalar(query)

    async def get_all(self) -> list["Role"]:
        """
        Возвращает все роли из базы данных.

        :return: Список моделей Role.
        """
        query = select(Role).order_by(Role.id)
        return await self.select_query_to_list(query)
