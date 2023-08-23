from collections.abc import AsyncIterator, Awaitable, Callable
from typing import Any, Final, Union

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from bot.database.repository.repository import Repository


SESSION_KEY: Final[str] = "session"
REPOSITORY_KEY: Final[str] = "repo"


class RepositoryMiddleware(BaseMiddleware):
    def __init__(
        self,
        session_pool: Union[
            async_sessionmaker[AsyncSession],
            Callable[[], AsyncIterator[AsyncSession]]
        ],
        session_key: str = SESSION_KEY,
        repo_key: str = REPOSITORY_KEY,
    ) -> None:
        self.session_pool = session_pool
        self.session_key = session_key
        self.repo_key = repo_key

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data[self.session_key] = session
            data[self.repo_key] = Repository(session)
            return await handler(event, data)
