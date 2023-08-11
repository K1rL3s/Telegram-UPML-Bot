import functools

from aiogram import types

from bot.database.db_funcs import Repository
from bot.utils.funcs import extract_username


def save_new_user(func):
    """
    Костыльный декоратор, который сохраняет или обновляет пользователей
    при их взаимодействии с ботом.
    """

    @functools.wraps(func)
    async def wrapper(
            event: types.Message | types.CallbackQuery,
            repo: Repository,
    ):
        await repo.save_new_user(
            event.from_user.id,
            extract_username(event)
        )
        return await func(event, repo)

    return wrapper
