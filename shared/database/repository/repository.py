from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from shared.database.repository import (
    ClassLessonsRepository,
    EducatorsScheduleRepository,
    FullLessonsRepository,
    LaundryRepository,
    MenuRepository,
    OlympRepository,
    RoleRepository,
    SettingsRepository,
    UniverRepository,
    UserRepository,
    UserRoleRepository,
)
from shared.database.repository.base_repo import BaseRepository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class Repository(BaseRepository):
    """Класс для вызова функций работы с базой данных."""

    def __init__(
        self,
        session: "AsyncSession",
    ) -> None:
        super().__init__(session)
        self.class_lessons = ClassLessonsRepository(session)
        self.educators = EducatorsScheduleRepository(session)
        self.full_lessons = FullLessonsRepository(session)
        self.user = UserRepository(session)
        self.role = RoleRepository(session)
        self.user_role = UserRoleRepository(session, self.user, self.role)
        self.settings = SettingsRepository(session)
        self.laundry = LaundryRepository(session)
        self.menu = MenuRepository(session)
        self.univers = UniverRepository(session)
        self.olymps = OlympRepository(session)

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
        await self.user.save_or_update_to_db(user_id, username)
        await self.settings.save_or_update_to_db(user_id)
        await self.laundry.save_or_update_to_db(user_id)
