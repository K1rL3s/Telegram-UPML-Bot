from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models.settings import Settings
from bot.database.repository.base_repo import BaseRepository


class SettingsRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_settings(self, user_id: int) -> Settings | None:
        """
        Возвращает Settings пользователя.

        :param user_id: ТГ Айди.
        :return: Модель Settings.
        """
        return await self._get_user_related_model(Settings, user_id)

    async def save_or_update_settings(
        self,
        user_id: int,
        **fields,
    ) -> None:
        """
        Создаёт или обнолвяет настройки пользователя.

        :param user_id: ТГ Айди.
        :param fields: Поле таблицы=значение.
        """

        if settings := await self.get_settings(user_id):
            for k, v in fields.items():
                setattr(settings, k, v)
        else:
            settings = Settings(user_id=user_id, **fields)
            self.session.add(settings)

        await self.session.commit()
