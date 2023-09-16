from typing import Any, TYPE_CHECKING

from aiogram.dispatcher.event.bases import UNHANDLED
from loguru import logger

from bot.middlewares.base import BaseInfoMiddleware

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from aiogram.types import CallbackQuery, Message, TelegramObject


class LoggingMiddleware(BaseInfoMiddleware):
    """Мидлварь для логов."""

    async def pre_callbackquery(
        self,
        callback: "CallbackQuery",
    ) -> None:
        """Лог при получении callback'а."""
        logger.debug(
            f'Получен callback "{callback.data}" '
            f"[{await self.get_short_info(callback)}]",
        )

    async def post_callbackquery(
        self,
        callback: "CallbackQuery",
        is_handled: bool,
    ) -> None:
        """Лог после обработки callback'а."""
        logger.debug(
            f'Отработан={is_handled} callback "{callback.data}" '
            f"[{await self.get_short_info(callback)}]",
        )

    async def pre_message(self, message: "Message") -> None:
        """Лог при получении сообщения."""
        if message.text:
            logger.debug(
                f'Получено message "{" ".join(message.text.split())}" '
                f"[{await self.get_short_info(message)}]",
            )
        elif message.photo:
            logger.debug(f"Получен photo [{await self.get_short_info(message)}]")

    async def post_message(self, message: "Message", is_handled: bool) -> None:
        """Лог после обработки сообщения."""
        if message.text:
            logger.debug(
                f'Отработан={is_handled} message "{" ".join(message.text.split())}" '
                f"[{await self.get_short_info(message)}]",
            )
        elif message.photo:
            logger.debug(
                f"Отработан={is_handled} photo [{await self.get_short_info(message)}]",
            )

    async def __call__(
        self,
        handler: "Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]",
        event: "TelegramObject",
        data: dict[str, Any],
    ) -> Any:
        class_name = event.__class__.__name__.lower()

        await getattr(self, f"pre_{class_name}")(event)
        result = await handler(event, data)
        await getattr(self, f"post_{class_name}")(event, not (result == UNHANDLED))

        return result
