"""Source: https://github.com/wakaree/simple_echo_bot."""
from typing import TYPE_CHECKING, Any, Union

from cachetools import TTLCache

from bot.middlewares.base import BaseInfoMiddleware

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from aiogram.types import CallbackQuery, Message


class ThrottlingMiddleware(BaseInfoMiddleware):
    """Мидлварь ограничения сообщений и нажатий кнопок в боте."""

    RATE_LIMIT = 0.5

    def __init__(self, rate_limit: float = RATE_LIMIT) -> None:
        self.cache = TTLCache(maxsize=10_000, ttl=rate_limit)

    async def __call__(
        self,
        handler: "Callable[[Message | CallbackQuery, dict[str, Any]], Awaitable[Any]]",
        event: "Union[Message, CallbackQuery]",
        data: dict[str, Any],
    ) -> Any:
        if (user := data.get("event_from_user")) is not None:
            if user.id in self.cache:
                return

            self.cache[event.from_user.id] = None

        return await handler(event, data)
