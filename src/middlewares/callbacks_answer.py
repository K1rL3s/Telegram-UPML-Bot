from typing import Any, Awaitable, Callable

from aiogram import types

from src.middlewares.base import MyBaseMiddleware


class CallbackQueryAnswerMiddleware(MyBaseMiddleware):
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
        # noinspection PyBroadException
        try:
            await event.answer()
        except Exception:
            pass
        return await handler(event, data)
