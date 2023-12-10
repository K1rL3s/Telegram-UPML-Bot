"""Модуль мидлварей."""

from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.middlewares.outer.album import AlbumsMiddleware
from bot.middlewares.outer.callback_answer import CallbackAnswerMiddleware
from bot.middlewares.outer.logging import LoggingMiddleware
from bot.middlewares.outer.repository import RepositoryMiddleware
from bot.middlewares.outer.throttling import ThrottlingMiddleware
from bot.middlewares.session.request import RetryRequestMiddleware

if TYPE_CHECKING:
    from aiogram import Bot, Dispatcher


__all__ = ("setup_global_middlewares",)


def setup_global_middlewares(
    bot: "Bot",
    dp: "Dispatcher",
    session_maker: "async_sessionmaker[AsyncSession]",
) -> None:
    """Регистрация мидлварей в боте и диспетчере."""
    bot.session.middleware(RetryRequestMiddleware())

    dp.message.outer_middleware(LoggingMiddleware())
    dp.callback_query.outer_middleware(LoggingMiddleware())

    dp.callback_query.outer_middleware(CallbackAnswerMiddleware())

    dp.message.outer_middleware(AlbumsMiddleware())

    dp.message.outer_middleware(ThrottlingMiddleware())
    dp.callback_query.outer_middleware(ThrottlingMiddleware())

    dp.message.outer_middleware(RepositoryMiddleware(session_maker))
    dp.callback_query.outer_middleware(RepositoryMiddleware(session_maker))
