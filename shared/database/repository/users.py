from enum import Enum
from typing import Any, Optional, Union

import sqlalchemy as sa
from loguru import logger
from sqlalchemy.orm import MappedColumn

from shared.database.models.settings import Settings
from shared.database.models.users import User
from shared.database.repository.base_repo import BaseRepository
from shared.utils.enums import RoleEnum


class UserRepository(BaseRepository):
    """Класс для работы с пользователями в базе данных."""

    async def get(self, user_id: int) -> "Optional[User]":
        """
        Возвращает пользователя.

        :param user_id: ТГ Айди.
        :return: Модель User.
        """
        query = sa.select(User).where(User.user_id == user_id)
        return await self._session.scalar(query)

    async def get_by_conditions(
        self,
        values: "list[tuple[MappedColumn[Any], Any]]",
        or_mode: bool = False,
    ) -> list["User"]:
        """
        Cписок Userов, у которых значение в Settings или User совпадает с переданным.

        :param values: Список из кортежей,
                       где первый элемент - колонка таблицы, второй - значение.
                       Пустой список - все юзеры.
        :param or_mode: Если True, то совпадение хотя бы по одному условию.
        :return: Список юзеров.
        """
        conditions = [column == value for column, value in values]  # !! [] ?
        query_conditions = sa.or_(*conditions) if or_mode else sa.and_(*conditions)
        query = sa.select(User).join(Settings).where(query_conditions)

        return await self.select_query_to_list(query)

    async def get_user_ids_by_username(
        self,
        username: str,
    ) -> list[int]:
        """
        Возвращает айди пользователя по его имени в базе.

        :param username: Имя юзера.
        :return: Айди юзера.
        """
        query = sa.select(User.user_id).where(User.username == username)
        return await self.select_query_to_list(query)

    async def save_or_update_to_db(
        self,
        user_id: int,
        username: str,
    ) -> None:
        """
        Сохраняет пользователя в базе данных.

        Если пользователь уже существует, то обновляет статус ``is_active`` и никнейм,

        :param user_id: Айди юзера.
        :param username: Имя пользователя.
        """
        if (user := await self.get(user_id)) is None:
            user = User(user_id=user_id, username=username)
            self._session.add(user)
            logger.info("Новый пользователь {user}", user=user)
        elif user.should_be_updated(username):
            user.is_active = True
            user.username = username

        await self._session.flush()

    async def update(
        self,
        user_id: int,
        **fields: Any,
    ) -> None:
        """
        Обновление пользователя по айди.

        :param user_id: ТГ Айди юзера.
        :param fields: Поле таблицы=значение, ...
        """
        query = sa.update(User).where(User.user_id == user_id).values(**fields)
        await self._session.execute(query)
        await self._session.flush()

    async def is_has_any_role(
        self,
        user_id: int,
        roles: "list[Union[RoleEnum, str]]",
    ) -> bool:
        """
        Имеет ли юзер хотя бы одну роль из переданных.

        :param user_id: ТГ Айди юзера.
        :param roles: Список ролей.
        :return: Тру или фэлс.
        """
        if (user := await self.get(user_id)) is None:
            return False

        role_names = [role.value if isinstance(role, Enum) else role for role in roles]
        return any(role.role in role_names for role in user.roles)
