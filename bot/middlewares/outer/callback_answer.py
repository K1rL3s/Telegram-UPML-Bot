import contextlib
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.exceptions import TelegramAPIError
from aiogram.types import CallbackQuery

from bot.middlewares.base import BaseInfoMiddleware


class CallbackAnswerMiddleware(BaseInfoMiddleware):
    """Мидлварь, который отвечает на callback query за меня."""

    async def __call__(
        self,
        handler: "Callable[[CallbackQuery, dict[str, Any]], Awaitable[Any]]",
        event: "CallbackQuery",
        data: dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        finally:
            with contextlib.suppress(TelegramAPIError):
                await event.answer()
