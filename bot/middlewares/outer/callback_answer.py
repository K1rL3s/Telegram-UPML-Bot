import contextlib
from typing import TYPE_CHECKING, Any

from aiogram.exceptions import TelegramAPIError

from bot.middlewares.base import BaseInfoMiddleware

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from aiogram.types import CallbackQuery


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
