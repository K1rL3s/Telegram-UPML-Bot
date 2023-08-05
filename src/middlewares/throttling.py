from typing import Any, Awaitable, Callable

from aiogram import types
from cachetools import TTLCache
from loguru import logger

from src.middlewares.base import MyBaseMiddleware


class ThrottlingMiddleware(MyBaseMiddleware):
    caches = TTLCache(maxsize=10_000, ttl=0.5)

    async def __call__(
            self,
            handler: Callable[
                [types.Message | types.CallbackQuery, dict[str, Any]],
                Awaitable[Any]
            ],
            event: types.Message | types.CallbackQuery,
            data: dict[str, Any],
    ) -> Any:
        if event.from_user.id in self.caches:
            return await self.message_throtled(event)

        self.caches[event.from_user.id] = None
        return await handler(event, data)

    async def message_throtled(
            self,
            message: types.Message | types.CallbackQuery
    ) -> None:
        logger.debug(f'Тротлинг [{await self.get_short_info(message)}]')
