from typing import TYPE_CHECKING

from bot.database.repository import (
    EducatorsScheduleRepository,
    LaundryRepository,
    LessonsRepository,
    MenuRepository,
    RoleRepository,
    SettingsRepository,
    UserRepository,
    UserRoleRepository,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class Repository:
    """Класс для вызова функций работы с базой данных."""

    def __init__(
        self,
        session: "AsyncSession",
    ) -> None:
        self._session = session
        self.user = UserRepository(session)
        self.role = RoleRepository(session)
        self.user_role = UserRoleRepository(session, self.user, self.role)
        self.settings = SettingsRepository(session)
        self.laundry = LaundryRepository(session)
        self.menu = MenuRepository(session)
        self.lessons = LessonsRepository(session)
        self.educators = EducatorsScheduleRepository(session)

    async def save_new_user_to_db(
        self,
        user_id: int,
        username: str,
    ) -> None:
        """
        Сохранение нового пользователя или обновление никнейма существующего.

        :param user_id: ТГ Айди.
        :param username: Имя пользователя.
        """
        await self.user.save_new_to_db(user_id, username)
        await self.settings.save_or_update_to_db(user_id)
        await self.laundry.save_or_update_to_db(user_id)
