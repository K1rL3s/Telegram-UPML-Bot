"""Модуль мидлварей."""

from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from bot.middlewares.session.request import RetryRequestMiddleware
from bot.middlewares.outer.logging import LoggingMiddleware
from bot.middlewares.outer.callbacks_answer import CallbackAnswerMiddleware
from bot.middlewares.outer.throttling import ThrottlingMiddleware
from bot.middlewares.outer.repository import RepositoryMiddleware
from bot.middlewares.inner.album import AlbumMiddleware

if TYPE_CHECKING:
    from aiogram import Bot, Dispatcher


__all__ = ("setup_middlewares",)


def setup_middlewares(
    bot: "Bot",
    dp: "Dispatcher",
    session_maker: "async_sessionmaker[AsyncSession]",
) -> None:
    """Регистрация мидлварей в боте и диспетчере."""
    bot.session.middleware(RetryRequestMiddleware())

    dp.message.outer_middleware(LoggingMiddleware())
    dp.callback_query.outer_middleware(LoggingMiddleware())

    dp.callback_query.outer_middleware(CallbackAnswerMiddleware())

    dp.message.outer_middleware(ThrottlingMiddleware())
    dp.callback_query.outer_middleware(ThrottlingMiddleware())

    dp.message.outer_middleware(RepositoryMiddleware(session_maker))
    dp.callback_query.outer_middleware(RepositoryMiddleware(session_maker))

    dp.message.middleware(AlbumMiddleware())
