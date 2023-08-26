from typing import Any, Optional, TYPE_CHECKING

from sqlalchemy import select

from bot.database.models.laundries import Laundry
from bot.database.repository.base_repo import BaseRepository
from bot.utils.datehelp import datetime_now

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class LaundryRepository(BaseRepository):
    """Класс для работы с таймерами прачечной в базе данных."""

    def __init__(self, session: "AsyncSession") -> None:
        self.session = session

    async def get(self, user_id: int) -> "Optional[Laundry]":
        """
        Возвращает Laundry пользователя.

        :param user_id: ТГ Айди.
        :return: Модель Laundry.
        """
        return await self._get_user_related_model(Laundry, user_id)

    async def get_expired(self) -> list["Laundry"]:
        """
        Возвращает список моделей Laundry, у которых пришло время для уведомления.

        :return: Список с Laundry.
        """
        now = datetime_now()
        query = select(Laundry).where(
            Laundry.is_active == True, Laundry.end_time <= now  # noqa
        )
        return list((await self.session.scalars(query)).all())

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
            self.session.add(laundry)

        await self.session.commit()
