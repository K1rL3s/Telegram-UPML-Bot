from typing import Any, Optional

from sqlalchemy import select

from shared.database.models.settings import Settings
from shared.database.repository.base_repo import BaseRepository


class SettingsRepository(BaseRepository):
    """Класс для работы с настройками пользователей в базе данных."""

    async def get(self, user_id: int) -> "Optional[Settings]":
        """
        Возвращает Settings пользователя.

        :param user_id: ТГ Айди.
        :return: Модель Settings.
        """
        query = select(Settings).where(Settings.user_id == user_id)
        return await self._session.scalar(query)

    async def save_or_update_to_db(
        self,
        user_id: int,
        **fields: Any,
    ) -> None:
        """
        Создаёт или обновляет настройки пользователя.

        :param user_id: ТГ Айди.
        :param fields: Ключ - колонка, значение - новое значение.
        """
        if settings := await self.get(user_id):
            for k, v in fields.items():
                setattr(settings, k, v)
        else:
            settings = Settings(user_id=user_id, **fields)
            self._session.add(settings)

        await self._session.flush()
