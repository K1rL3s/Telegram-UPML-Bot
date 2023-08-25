"""Source: https://github.com/wakaree/simple_echo_bot."""
from typing import Any, TYPE_CHECKING, Union

from cachetools import TTLCache
from loguru import logger

from bot.middlewares.base import MyBaseMiddleware

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from aiogram.types import CallbackQuery, Message


class ThrottlingMiddleware(MyBaseMiddleware):
    """Мидлварь ограничения сообщений и нажатий кнопок в боте."""

    RATE_LIMIT = 0.5

    def __init__(self, rate_limit: float = RATE_LIMIT) -> None:
        self.cache = TTLCache(maxsize=10_000, ttl=rate_limit)

    async def message_throttled(self, message: "Union[Message, CallbackQuery]") -> None:
        """Лог при троттлинге, может быть надо убрать."""
        logger.debug(f"Троттлинг [{await self.get_short_info(message)}]")

    async def __call__(
        self,
        handler: "Callable[[Message | CallbackQuery, dict[str, Any]], Awaitable[Any]]",
        event: "Message | CallbackQuery",
        data: dict[str, Any],
    ) -> Any:
        if (user := data.get("event_from_user")) is not None:
            if user.id in self.cache:
                return await self.message_throttled(event)

            self.cache[event.from_user.id] = None

        return await handler(event, data)
