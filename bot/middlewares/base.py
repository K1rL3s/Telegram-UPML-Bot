from abc import ABC
from typing import Union

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from bot.utils.funcs import extract_username


class MyBaseMiddleware(BaseMiddleware, ABC):
    """Базовый мидлварь. Он нужен, чтобы метод get_short_info был везде."""

    @staticmethod
    async def get_short_info(message: "Union[Message, CallbackQuery]") -> str | None:
        username = extract_username(message)

        if isinstance(message, Message):
            return (
                f"id={message.from_user.id}, "
                f"chat={message.chat.id}, "
                f"username={username}"
            )

        if isinstance(message, CallbackQuery):
            return (
                f"id={message.from_user.id}, "
                f"chat={message.message.chat.id}, "
                f"username={username}"
            )

        raise RuntimeError(
            "An invalid argument was passed - not a Message or CallbackQuery.",
        )
