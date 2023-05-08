from aiogram import Dispatcher
from aiogram.utils.exceptions import MessageToEditNotFound, MessageNotModified
from loguru import logger


async def message_editing(*_):
    """
    Юзер может удалить сообщение бота, пока бот грузит инфу.
    Юзер может нажать на "Сегодня" несколько раз подряд.
    """
    return True


async def all_errors(update, error):
    logger.error(f'Exception Error: {error}, {update=}')


def register_errors(dp: Dispatcher):
    dp.register_errors_handler(
        message_editing, exception=MessageToEditNotFound
    )
    dp.register_errors_handler(
        message_editing, exception=MessageNotModified
    )
    dp.register_errors_handler(
        all_errors, exception=Exception
    )
