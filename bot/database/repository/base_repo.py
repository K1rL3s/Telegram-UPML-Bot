from abc import ABC

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models.base_models import UserRelatedModel


class BaseRepository(ABC):
    session: AsyncSession

    async def _get_user_related_model(
        self,
        model: type[UserRelatedModel],
        user_id: int,
    ) -> UserRelatedModel | None:
        """
        Возвращает связанную с юзером модель по айди пользователя.

        :param model: Модель-наследник от UserRelatedModel.
        :param user_id: ТГ Айди юзера.
        :return: Модель model.
        """

        # noinspection PyTypeChecker
        query = sa.select(model).where(model.user_id == user_id)
        return await self.session.scalar(query)
