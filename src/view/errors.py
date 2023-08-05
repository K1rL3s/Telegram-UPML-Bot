from aiogram import Router
from aiogram.types import ErrorEvent
from loguru import logger


router = Router(name='errors')


@router.errors()
async def all_errors(exception: ErrorEvent):
    logger.error(f'Exception Error: {exception.exception}, {exception.update}')
