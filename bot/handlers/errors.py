from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import ExceptionTypeFilter
from loguru import logger

if TYPE_CHECKING:
    from aiogram.types import ErrorEvent


router = Router(name=__name__)


@router.errors(
    ExceptionTypeFilter(TelegramBadRequest),
    F.exception.message.contains("is not modified"),
)
async def not_modified_error(_: "ErrorEvent") -> bool:
    """
    Сообщение не было изменено.

    Возникает, если нажать "сегодня" при просмотре расписаний на сегодня.
    """
    logger.debug("Message is not modified")
    return True


@router.errors()
async def all_errors(event: "ErrorEvent") -> None:
    """Логгер всех ошибок при обработке событий телеграма."""
    logger.exception(f"Exception while handling: {event.exception} | {event.update}")
