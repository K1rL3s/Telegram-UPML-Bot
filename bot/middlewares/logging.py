from typing import Any, Awaitable, Callable

from aiogram import types
from loguru import logger

from bot.middlewares.base import MyBaseMiddleware


class LoggingMiddleware(MyBaseMiddleware):
    """
    Мидлварь для логов.
    """

    async def __call__(
            self,
            handler: Callable[
                [types.TelegramObject, dict[str, Any]],
                Awaitable[Any]
            ],
            event: types.TelegramObject,
            data: dict[str, Any],
    ):
        class_name = event.__class__.__name__.lower()
        await getattr(self, f'start_{class_name}')(event)
        result = await handler(event, data)
        await getattr(self, f'end_{class_name}')(event)
        return result

    async def start_callbackquery(self, callback: types.CallbackQuery):
        logger.debug(
            f'Вызван callback "{callback.data}" '
            f'[{await self.get_short_info(callback)}]'
        )

    async def end_callbackquery(self, callback: types.CallbackQuery, ):
        logger.debug(
            f'Отработан callback "{callback.data}" '
            f'[{await self.get_short_info(callback)}]'
        )

    async def start_message(self, message: types.Message):
        if message.text:
            logger.debug(
                f'Получено сообщение "{" ".join(message.text.split())}" '
                f'[{await self.get_short_info(message)}]'
            )
        elif message.photo:
            logger.debug(
                f'Получено изображение '
                f'[{await self.get_short_info(message)}]'
            )

    async def end_message(self, message: types.Message):
        if message.text:
            logger.debug(
                f'Отработано сообщение "{" ".join(message.text.split())}" '
                f'[{await self.get_short_info(message)}]'
            )
        elif message.photo:
            logger.debug(
                f'Отработано изображение '
                f'[{await self.get_short_info(message)}]'
            )