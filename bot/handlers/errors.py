from aiogram import Router
from aiogram.types import ErrorEvent
from loguru import logger


router = Router(name=__name__)


@router.errors()
async def all_errors(exception: ErrorEvent):
    logger.error(f"Exception Error: {exception.exception}, {exception.update}")
