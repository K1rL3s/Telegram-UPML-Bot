from typing import TYPE_CHECKING, Union

from aiogram.filters import Filter

from bot.database.repository.repository import Repository
from bot.database.db_session import get_session
from bot.utils.funcs import extract_username

if TYPE_CHECKING:
    from aiogram.types import CallbackQuery, Message


class SaveUser(Filter):
    """Смешной фильтр, который сохраняет или обновляет пользователей в бд."""

    async def __call__(self, event: "Union[Message, CallbackQuery]") -> bool:
        async with get_session() as session:
            repo = Repository(session)
            await repo.save_new_user_to_db(event.from_user.id, extract_username(event))
        return True
