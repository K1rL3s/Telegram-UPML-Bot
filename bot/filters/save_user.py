from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from bot.database.repository.repository import Repository
from bot.database.db_session import get_session
from bot.utils.funcs import extract_username


class SaveUser(Filter):
    """
    Смешной фильтр, который работает вместо декоратора
    для сохранения или обновления пользователей бота.
    """

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        async with get_session() as session:
            repo = Repository(session)
            await repo.save_new_user(event.from_user.id, extract_username(event))
        return True
