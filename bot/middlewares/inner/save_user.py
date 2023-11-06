from typing import TYPE_CHECKING, Any

from bot.middlewares.base import BaseInfoMiddleware
from bot.utils.funcs import extract_username

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from aiogram.types import Message

    from bot.database.repository.repository import Repository


class SaveUpdateUserMiddleware(BaseInfoMiddleware):
    """
    Мидлварь, который сохраняет или обновляет информацию о пользователе в бд.

    Используется в bot/handlers/client/start.py и settings.py,
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
