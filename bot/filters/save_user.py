from typing import TYPE_CHECKING, Union

from aiogram.filters import Filter

from bot.utils.funcs import extract_username

if TYPE_CHECKING:
    from aiogram.types import CallbackQuery, Message

    from bot.database.repository.repository import Repository


class SaveUpdateUser(Filter):
    """Смешной фильтр, который сохраняет или обновляет пользователей в бд."""

    async def __call__(
        self,
        event: "Union[Message, CallbackQuery]",
        repo: "Repository",
    ) -> bool:
        await repo.save_new_user_to_db(event.from_user.id, extract_username(event))
        return True
