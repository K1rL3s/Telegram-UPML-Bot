from typing import TYPE_CHECKING

from aiogram import Router
from loguru import logger

if TYPE_CHECKING:
    from aiogram.types import ErrorEvent

router = Router(name=__name__)


@router.errors()
async def all_errors(exception: "ErrorEvent") -> None:
    """Логгер всех ошибок при обработке событий телеграма."""
    logger.error(f"Exception Error: {exception.exception}, {exception.update}")
