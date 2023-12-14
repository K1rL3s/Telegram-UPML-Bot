import contextlib
from typing import TYPE_CHECKING, Union

import sqlalchemy as sa

from shared.database.models import User
from shared.database.repository.base_repo import BaseRepository
from shared.utils.enums import Roles

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from shared.database.repository import RoleRepository, UserRepository


class UserRoleRepository(BaseRepository):
    """Класс для работы с ролями и пользователями в базе данных."""

    def __init__(
        self,
        session: "AsyncSession",
        user_repo: "UserRepository",
        role_repo: "RoleRepository",
    ) -> None:
        self._session = session
        self._user = user_repo
        self._role = role_repo

    async def get_users_with_any_roles(
        self,
    ) -> list["User"]:
        """
        Возвращает всех пользователей, у которых есть какая-либо роль.

        :return: Список юзеров.
        """

        query = sa.select(User).join(User.roles).distinct()

        return await self.select_query_to_list(query)

    async def remove_role_from_user(
        self,
        user_id: int,
        role: "Union[Roles | str]",
    ) -> None:
        """
        Удаляет роль у юзера.

        :param user_id: ТГ Айди юзера.
        :param role: Его роль.
        """
        if isinstance(role, Roles):
            role = role.value

        user = await self._user.get(user_id)
        role = await self._role.get(role)

        with contextlib.suppress(ValueError):
            user.roles.remove(role)

        await self._session.flush()

    async def remove_all_roles_from_user(
        self,
        user_id: int,
    ) -> None:
        """
        Удаляет все роли у юзера.

        :param user_id: ТГ Айди юзера.
        """
        user = await self._user.get(user_id)

        user.roles.clear()

        await self._session.flush()

    async def add_role_to_user(
        self,
        user_id: int,
        role: Roles | str,
    ) -> None:
        """
        Добавляет роль юзеру.

        :param user_id: ТГ Айди юзера.
        :param role: Роль.
        """
        if isinstance(role, Roles):
            role = role.value

        user = await self._user.get(user_id)
        role = await self._role.get(role)

        user.roles.append(role)

        await self._session.flush()
