"""
Модуль мидлварей.
"""

from aiogram import Dispatcher

from src.middlewares.throttling import ThrottlingMiddleware
from src.middlewares.logging import LoggingMiddleware
from src.middlewares.callbacks_answer import CallbackQueryAnswerMiddleware


def setup_middlewares(dp: Dispatcher) -> None:
    dp.setup_middleware(ThrottlingMiddleware())
    dp.middleware.setup(LoggingMiddleware())
    dp.middleware.setup(CallbackQueryAnswerMiddleware())
