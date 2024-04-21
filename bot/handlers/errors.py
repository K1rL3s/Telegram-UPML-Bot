from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from loguru import logger

router = Router(name=__name__)


@router.errors(
    ExceptionTypeFilter(TelegramBadRequest),
    F.exception.message.contains("is not modified"),
)
async def not_modified_error(_: "ErrorEvent") -> None:
    """
    Сообщение не было изменено.

    Возникает, если нажать "сегодня" при просмотре расписаний на сегодня.
    """
    logger.debug("Message is not modified")


@router.errors()
async def all_errors(event: "ErrorEvent") -> None:
    """Логгер всех ошибок при обработке событий телеграма."""
    # f-строка, потому что loguru cannot pickle 'weakref.ReferenceType' object
    logger.error(
        f"Exception while handling: {repr(event.exception)} | {event.update}",
    )
