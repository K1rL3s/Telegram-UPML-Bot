from enum import Enum
from typing import TYPE_CHECKING, Union

from sqlalchemy import select

from bot.database.models.roles import Role
from bot.database.repository.base_repo import BaseRepository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from bot.utils.enums import Roles


class RoleRepository(BaseRepository):
    """Класс для работы с ролями в базе данных."""

    def __init__(self, session: "AsyncSession") -> None:
        self._session = session

    async def get(
        self,
        role: "Union[Roles | str]",
    ) -> Role | None:
        """
        Возвращает модель Role по названию роли.

        :param role: Название роли.
        :return: Модель Role.
        """
        if isinstance(role, Enum):
            role = role.value

        role_query = select(Role).where(Role.role == role)
        return await self._session.scalar(role_query)
