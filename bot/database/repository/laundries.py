import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models.laundries import Laundry
from bot.database.repository.base_repo import BaseRepository
from bot.utils.datehelp import datetime_now


class LaundryRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_laundry(self, user_id: int) -> Laundry | None:
        """
        Возвращает Laundry пользователя.

        :param user_id: ТГ Айди.
        :return: Модель Laundry.
        """
        return await self._get_user_related_model(Laundry, user_id)

    async def get_expired_laundries(self) -> list[Laundry]:
        """
        Возвращает список моделей Laundry,
        у которых пришло время для уведомления.

        :return: Список из Laundry.
        """

        now = datetime_now()
        query = sa.select(Laundry).where(
            Laundry.is_active == True, Laundry.end_time <= now  # noqa
        )
        return list((await self.session.scalars(query)).all())

    async def save_or_update_laundry(
        self,
        user_id: int,
        **fields,
    ) -> None:
        """
        Сохраняет или обновляет уведомление о стирке/сушке.

        :param user_id: ТГ Айди.
        :param fields: Поле таблицы=значение.
        """

        if laundry := await self.get_laundry(user_id):
            for k, v in fields.items():
                setattr(laundry, k, v)
        else:
            laundry = Laundry(user_id=user_id, **fields)
            self.session.add(
                laundry,
            )

        await self.session.commit()
