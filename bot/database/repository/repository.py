import contextlib
from typing import TYPE_CHECKING, Union

from bot.database.repository import (
    ClassLessonsRepository,
    EducatorsScheduleRepository,
    FullLessonsRepository,
    LaundryRepository,
    MenuRepository,
    RoleRepository,
    SettingsRepository,
    UserRepository,
)
from bot.utils.datehelp import date_by_format
from bot.utils.enums import Roles

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from bot.types import LessonsCollection


class Repository:
    """Класс для вызова функций работы с базой данных."""

    def __init__(
        self,
        session: "AsyncSession",
    ) -> None:
        self._session = session
        self.class_lessons = ClassLessonsRepository(session)
        self.educators = EducatorsScheduleRepository(session)
        self.full_lessons = FullLessonsRepository(session)
        self.laundry = LaundryRepository(session)
        self.menu = MenuRepository(session)
        self.role = RoleRepository(session)
        self.settings = SettingsRepository(session)
        self.user = UserRepository(session)

    async def save_new_user_to_db(
        self,
        user_id: int,
        username: str,
    ) -> None:
        """
        Сохранение нового пользователя или обновление никнейма и статуса существующего.

        :param user_id: ТГ Айди.
        :param username: Имя пользователя.
        """
        await self.user.save_new_to_db(user_id, username)
        await self.settings.save_or_update_to_db(user_id)
        await self.laundry.save_or_update_to_db(user_id)

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

        user = await self.user.get(user_id)
        role = await self.role.get(role)

        with contextlib.suppress(ValueError):
            user.roles.remove(role)

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

        user = await self.user.get(user_id)
        role = await self.role.get(role)

        user.roles.append(role)

        await self._session.flush()

    async def save_lessons_collection_to_db(
        self,
        lessons: "LessonsCollection",
    ) -> None:
        """
        Сохраняет готовые изображения расписаний уроков на дату для параллели.

        :param lessons: Полное изображение расписания уроков.
        """
        await self.full_lessons.save_or_update_to_db(
            lessons.full_photo_id,
            date_by_format(lessons.date),
            lessons.grade,
        )
        for class_photo_id, letter in zip(lessons.class_photo_ids, "АБВ"):
            await self.class_lessons.save_or_update_to_db(
                class_photo_id,
                date_by_format(lessons.date),
                lessons.grade,
                letter,
            )
