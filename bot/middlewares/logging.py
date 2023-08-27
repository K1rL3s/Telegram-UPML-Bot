from typing import Any, TYPE_CHECKING

from loguru import logger

from bot.middlewares.base import MyBaseMiddleware

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from aiogram.types import CallbackQuery, Message, TelegramObject


class LoggingMiddleware(MyBaseMiddleware):
    """Мидлварь для логов."""

    async def start_callbackquery(self, callback: "CallbackQuery") -> None:
        """Лог при старте обработки callback'а."""
        logger.debug(
            f'Вызван callback "{callback.data}" '
            f"[{await self.get_short_info(callback)}]",
        )

    async def end_callbackquery(self, callback: "CallbackQuery") -> None:
        """Лог после обработки callback'а."""
        logger.debug(
            f'Отработан callback "{callback.data}" '
            f"[{await self.get_short_info(callback)}]",
        )

    async def start_message(self, message: "Message") -> None:
        """Лог при старте обработки сообщения."""
        if message.text:
            logger.debug(
                f'Получено сообщение "{" ".join(message.text.split())}" '
                f"[{await self.get_short_info(message)}]",
            )
        elif message.photo:
            logger.debug(f"Получено изображение [{await self.get_short_info(message)}]")

    async def end_message(self, message: "Message") -> None:
        """Лог после обработки сообщения."""
        if message.text:
            logger.debug(
                f'Отработано сообщение "{" ".join(message.text.split())}" '
                f"[{await self.get_short_info(message)}]",
            )
        elif message.photo:
            logger.debug(
                f"Отработано изображение [{await self.get_short_info(message)}]",
            )

    async def __call__(
        self,
        handler: "Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]",
        event: "TelegramObject",
        data: dict[str, Any],
    ) -> Any:
        class_name = event.__class__.__name__.lower()

        await getattr(self, f"start_{class_name}")(event)
        result = await handler(event, data)
        await getattr(self, f"end_{class_name}")(event)

        return result
