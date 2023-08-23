from sqlalchemy.ext.asyncio import AsyncSession

from bot.utils.consts import Roles
from bot.database.repository import (
    EducatorsScheduleRepository,
    RoleRepository,
    SettingsRepository,
    LessonsRepository,
    LaundryRepository,
    UserRepository,
    MenuRepository,
)


class Repository:
    """
    Класс для вызова функций работы с базой данных.
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session
        self.user = UserRepository(session)
        self.settings = SettingsRepository(session)
        self.laundry = LaundryRepository(session)
        self.menu = MenuRepository(session)
        self.lessons = LessonsRepository(session)
        self.educators = EducatorsScheduleRepository(session)
        self.role = RoleRepository(session)

    async def save_new_user(
        self,
        user_id: int,
        username: str,
    ) -> None:
        """
        Сохранение нового пользователя или обновление никнейма существующего.

        :param user_id: ТГ Айди.
        :param username: Имя пользователя.
        """
        await self.user.save_new_user(user_id, username)
        await self.settings.save_or_update_settings(user_id)
        await self.laundry.save_or_update_laundry(user_id)

    async def remove_role_from_user(
        self,
        user_id: int,
        role: Roles | str,
    ) -> None:
        """
        Удаляет роль у юзера.

        :param user_id: ТГ Айди юзера.
        :param role: Его роль.
        """

        if isinstance(role, Roles):
            role = role.value

        user = await self.user.get_user(user_id)
        role = await self.role.get_role(role)

        try:
            user.roles.remove(role)
        except ValueError:
            pass

        await self.session.commit()

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

        user = await self.user.get_user(user_id)
        role = await self.role.get_role(role)

        user.roles.append(role)

        await self.session.commit()
