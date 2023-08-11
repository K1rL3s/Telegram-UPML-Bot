"""
Модуль мидлварей.
"""

from aiogram import Dispatcher

from bot.database.db_session import get_session
from .repository import RepositoryMiddleware
from .album import AlbumMiddleware
from .throttling import ThrottlingMiddleware
from .logging import LoggingMiddleware
from .callbacks_answer import CallbackAnswerMiddleware


def setup_middlewares(dp: Dispatcher) -> None:
    dp.message.middleware(RepositoryMiddleware(get_session))
    dp.callback_query.middleware(RepositoryMiddleware(get_session))

    dp.message.middleware(AlbumMiddleware())

    dp.message.middleware(ThrottlingMiddleware())
    dp.callback_query.middleware(ThrottlingMiddleware())

    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())

    dp.callback_query.middleware(CallbackAnswerMiddleware())
