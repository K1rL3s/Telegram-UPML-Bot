import aiogram
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware


class MyBaseMiddleware(BaseMiddleware):
    """
    Базовый мидлварь. Он нужен, чтобы метод get_short_info был везде.
    """

    @staticmethod
    async def get_state() -> str | None:
        return await aiogram.Dispatcher.get_current().storage.get_state(
            chat=types.Chat.get_current().id,
            user=types.User.get_current().id
        )

    async def get_short_info(
            self, message: types.Message | types.CallbackQuery
    ):
        username = (message.from_user.username or
                    message.from_user.first_name or
                    message.from_user.last_name)  # XD
        state = await self.get_state()

        if isinstance(message, types.Message):
            return f'id={message.from_user.id}, ' \
                   f'chat={message.chat.id}, ' \
                   f'state={state}, ' \
                   f'username={username}'

        elif isinstance(message, types.CallbackQuery):
            return f'id={message.from_user.id}, ' \
                   f'chat={message.message.chat.id}, ' \
                   f'state={state}, ' \
                   f'username={username}'
