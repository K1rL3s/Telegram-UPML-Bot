from typing import Any, Final, TYPE_CHECKING

from aiogram import BaseMiddleware

from bot.database.repository.repository import Repository

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from aiogram.types import TelegramObject
    from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class RepositoryMiddleware(BaseMiddleware):
    """Мидлварь для добавления класса-репозитория в аргументы обработчиков телеграма."""

    SESSION_KEY: Final[str] = "session"
    REPOSITORY_KEY: Final[str] = "repo"

    def __init__(
        self,
        session_maker: "async_sessionmaker[AsyncSession]",
        session_key: str = SESSION_KEY,
        repository_key: str = REPOSITORY_KEY,
    ) -> None:
        self.session_maker = session_maker
        self.session_key = session_key
        self.repository_key = repository_key

    async def __call__(
        self,
        handler: "Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]",
        event: "TelegramObject",
        data: dict[str, Any],
    ) -> Any:
        async with self.session_maker() as session:
            data[self.session_key] = session
            data[self.repository_key] = Repository(session)
            return await handler(event, data)
