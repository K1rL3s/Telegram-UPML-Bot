from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.dispatcher.event.bases import REJECTED, UNHANDLED
from aiogram.types import CallbackQuery, Message, TelegramObject
from loguru import logger

from bot.middlewares.base import BaseInfoMiddleware


class LoggingMiddleware(BaseInfoMiddleware):
    """Мидлварь для логов."""

    async def pre_callbackquery(
        self,
        callback: "CallbackQuery",
    ) -> None:
        """Лог при получении callback'а."""
        logger.debug(
            'Get callback={id} "{data}" [{short_info}]',
            id=callback.id,
            data=callback.data,
            short_info=self.get_short_info(callback),
        )

    async def post_callbackquery(
        self,
        callback: "CallbackQuery",
        is_handled: bool,
    ) -> None:
        """Лог после обработки callback'а."""
        logger.debug(
            'Over={is_handled} callback={id} "{data}" [{short_info}]',
            is_handled=is_handled,
            id=callback.id,
            data=callback.data,
            short_info=self.get_short_info(callback),
        )

    async def pre_message(self, message: "Message") -> None:
        """Лог при получении сообщения."""
        if message.photo:
            log = 'Get photo={id} "{text}" [{short_info}]'
            text = " ".join(message.caption.split()) if message.caption else ""
        else:
            log = 'Get message={id} "{text}" [{short_info}]'
            text = " ".join(message.text.split())
        logger.debug(
            log,
            id=message.message_id,
            text=text,
            short_info=self.get_short_info(message),
        )

    async def post_message(self, message: "Message", is_handled: bool) -> None:
        """Лог после обработки сообщения."""
        if message.photo:
            log = 'Over={is_handled} photo={id} "{text}" [{short_info}]'
            text = " ".join(message.caption.split()) if message.caption else ""
        else:
            log = 'Over={is_handled} message={id} "{text}" [{short_info}]'
            text = " ".join(message.text.split())
        logger.debug(
            log,
            is_handled=is_handled,
            id=message.message_id,
            text=text,
            short_info=self.get_short_info(message),
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
        await getattr(self, f"post_{class_name}")(
            event,
            result not in (UNHANDLED, REJECTED),
        )
        return result
