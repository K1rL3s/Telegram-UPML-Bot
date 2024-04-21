from typing import Any, Optional

from sqlalchemy import select

from shared.database.models.laundries import Laundry
from shared.database.repository.base_repo import BaseRepository
from shared.utils.datehelp import datetime_now


class LaundryRepository(BaseRepository):
    """Класс для работы с таймерами прачечной в базе данных."""

    async def get(self, user_id: int) -> "Optional[Laundry]":
        """
        Возвращает Laundry пользователя.

        :param user_id: ТГ Айди.
        :return: Модель Laundry.
        """
        query = select(Laundry).where(Laundry.user_id == user_id)
        return await self._session.scalar(query)

    async def get_expired(self) -> list["Laundry"]:
        """
        Возвращает список моделей Laundry, у которых пришло время для уведомления.

        :return: Список с Laundry.
        """
        query = select(Laundry).where(
            Laundry.is_active == True,  # noqa
            Laundry.end_time <= datetime_now(),
        )
        return await self.select_query_to_list(query)

    async def save_or_update_to_db(
        self,
        user_id: int,
        **fields: Any,
    ) -> None:
        """
        Сохраняет или обновляет информацию о таймере прачечной.

        :param user_id: ТГ Айди.
        :param fields: Ключ - колонка, значение - новое значение.
        """
        if laundry := await self.get(user_id):
            for k, v in fields.items():
                setattr(laundry, k, v)
        else:
            laundry = Laundry(user_id=user_id, **fields)
            self._session.add(laundry)

        await self._session.flush()

    async def cancel_timer(
        self,
        user_id: int,
    ) -> None:
        await self.save_or_update_to_db(
            user_id,
            start_time=None,
            end_time=None,
            is_active=False,
            rings=None,
        )
