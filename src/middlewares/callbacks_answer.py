from aiogram import types
from aiogram.utils.exceptions import InvalidQueryID

from src.middlewares.base import MyBaseMiddleware


class CallbackQueryAnswerMiddleware(MyBaseMiddleware):
    """
    Мидлварь, который отвечает на callback query за меня.
    """

    @staticmethod
    async def on_post_process_callback_query(
            callback: types.CallbackQuery, *_
    ):
        try:
            await callback.answer()
        except InvalidQueryID:
            pass
