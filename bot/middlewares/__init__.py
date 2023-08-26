"""Модуль мидлварей."""

from typing import TYPE_CHECKING

from bot.database.db_session import get_session
from bot.middlewares.repository import RepositoryMiddleware
from bot.middlewares.album import AlbumMiddleware
from bot.middlewares.request import RetryRequestMiddleware
from bot.middlewares.throttling import ThrottlingMiddleware
from bot.middlewares.logging import LoggingMiddleware
from bot.middlewares.callbacks_answer import CallbackAnswerMiddleware

if TYPE_CHECKING:
    from aiogram import Bot, Dispatcher

__all__ = [
    "setup_middlewares",
]


def setup_middlewares(bot: "Bot", dp: "Dispatcher") -> None:
    """Регистрация мидлварей в боте и диспетчере."""
    bot.session.middleware(RetryRequestMiddleware())

    dp.message.middleware(RepositoryMiddleware(get_session))
    dp.callback_query.middleware(RepositoryMiddleware(get_session))

    dp.message.middleware(AlbumMiddleware())

    dp.message.middleware(ThrottlingMiddleware())
    dp.callback_query.middleware(ThrottlingMiddleware())

    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())

    dp.callback_query.middleware(CallbackAnswerMiddleware())
