from typing import Any, TYPE_CHECKING

from bot.middlewares.base import MyBaseMiddleware

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from aiogram.types import CallbackQuery


class CallbackAnswerMiddleware(MyBaseMiddleware):
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
            await event.answer()
