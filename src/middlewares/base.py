from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware, types

from src.utils.funcs import extract_username


class MyBaseMiddleware(BaseMiddleware):
    """
    Базовый мидлварь. Он нужен, чтобы метод get_short_info был везде.
    """

    async def __call__(
            self,
            handler: Callable[
                [types.TelegramObject, dict[str, Any]],
                Awaitable[Any]
            ],
            event: types.TelegramObject,
            data: dict[str, Any],
    ):
        return await handler(event, data)

    @staticmethod
    async def get_short_info(message: types.Message | types.CallbackQuery):
        username = extract_username(message)

        if isinstance(message, types.Message):
            return f'id={message.from_user.id}, ' \
                   f'chat={message.chat.id}, ' \
                   f'username={username}'

        elif isinstance(message, types.CallbackQuery):
            return f'id={message.from_user.id}, ' \
                   f'chat={message.message.chat.id}, ' \
                   f'username={username}'
