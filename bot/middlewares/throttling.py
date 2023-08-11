"""
Source:
https://github.com/wakaree/simple_echo_bot
"""

from typing import Any, Awaitable, Callable

from aiogram.types import Message, CallbackQuery, User
from cachetools import TTLCache
from loguru import logger

from bot.middlewares.base import MyBaseMiddleware


class ThrottlingMiddleware(MyBaseMiddleware):
    RATE_LIMIT = 0.5

    def __init__(self, rate_limit: float = RATE_LIMIT) -> None:
        self.cache = TTLCache(maxsize=10_000, ttl=rate_limit)

    async def __call__(
            self,
            handler: Callable[
                [Message | CallbackQuery, dict[str, Any]],
                Awaitable[Any]
            ],
            event: Message | CallbackQuery,
            data: dict[str, Any],
    ) -> Any:
        user: User | None = data.get("event_from_user")

        if user is not None:
            if user.id in self.cache:
                return await self.message_throtled(event)

            self.cache[event.from_user.id] = None

        return await handler(event, data)

    async def message_throtled(self, message: Message | CallbackQuery) -> None:
        logger.debug(f'Тротлинг [{await self.get_short_info(message)}]')
