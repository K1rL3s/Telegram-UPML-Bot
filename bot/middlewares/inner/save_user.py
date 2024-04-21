from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import Message

from bot.middlewares.base import BaseInfoMiddleware
from shared.database.repository.repository import Repository
from shared.utils.funcs import extract_username


class SaveUpdateUserMiddleware(BaseInfoMiddleware):
    """
    Мидлварь, который сохраняет или обновляет информацию о пользователе в бд.

    Используется в bot/handlers/client/start и bot/handlers/client/settings,
    чтобы юзер точно был в базе.
    """

    async def __call__(
        self,
        handler: "Callable[[Message, dict[str, Any]], Awaitable[Any]]",
        event: "Message",
        data: dict[str, Any],
    ) -> Any:
        repo: "Repository" = data["repo"]
        await repo.save_new_user_to_db(
            event.from_user.id,
            extract_username(event.from_user),
        )

        return await handler(event, data)
