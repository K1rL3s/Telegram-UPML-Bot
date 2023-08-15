from abc import ABC

from aiogram import BaseMiddleware, types

from bot.utils.funcs import extract_username


class MyBaseMiddleware(BaseMiddleware, ABC):
    """
    Базовый мидлварь. Он нужен, чтобы метод get_short_info был везде.
    """

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
