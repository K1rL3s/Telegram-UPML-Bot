from enum import Enum

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models.roles import Role
from bot.database.repository.base_repo import BaseRepository
from bot.utils.consts import Roles


class RoleRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_role(
        self,
        role: Roles | str,
    ) -> Role | None:
        """
        Возвращает модель Role по названию роли.

        :param role: Название роли.
        :return: Модель Role.
        """

        if isinstance(role, Enum):
            role = role.value

        role_query = sa.select(Role).where(Role.role == role)
        return await self.session.scalar(role_query)
