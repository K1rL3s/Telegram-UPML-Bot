"""
Модуль мидлварей.
"""

from aiogram import Dispatcher

from src.middlewares.throttling import ThrottlingMiddleware
from src.middlewares.logging import LoggingMiddleware
from src.middlewares.callbacks_answer import CallbackQueryAnswerMiddleware


def setup_middlewares(dp: Dispatcher) -> None:
    dp.message.middleware(ThrottlingMiddleware())
    dp.callback_query.middleware(ThrottlingMiddleware())
    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())
    dp.callback_query.middleware(CallbackQueryAnswerMiddleware())
