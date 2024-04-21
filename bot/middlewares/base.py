from abc import ABC
from typing import Union

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from shared.utils.funcs import extract_username


class BaseInfoMiddleware(BaseMiddleware, ABC):
    """Базовый мидлварь. Он нужен, чтобы метод get_short_info был везде."""

    @staticmethod
    def get_short_info(message: "Union[Message, CallbackQuery]") -> str | None:
        """Короткая информация о пользователе для логов."""
        return (
            f"id={message.from_user.id}, "
            f"username={extract_username(message.from_user)}"
        )
