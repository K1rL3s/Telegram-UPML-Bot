from typing import Any, Awaitable, Callable

from aiogram import types

from bot.middlewares.base import MyBaseMiddleware


class CallbackAnswerMiddleware(MyBaseMiddleware):
    """
    Мидлварь, который отвечает на callback query за меня.
    """

    async def __call__(
            self,
            handler: Callable[
                [types.CallbackQuery, dict[str, Any]],
                Awaitable[Any]
            ],
            event: types.CallbackQuery,
            data: dict[str, Any],
    ):
        try:
            return await handler(event, data)
        finally:
            await event.answer()
