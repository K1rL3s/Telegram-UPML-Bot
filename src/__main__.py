import asyncio
from pathlib import Path

from aiogram import Dispatcher, Bot, executor
from loguru import logger
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy.orm import close_all_sessions

from src.database.db_session import global_init
from src.schedule import run_schedule_jobs
from src.utils.consts import Config
from src.view import register_view
from src.middlewares import setup_middlewares


async def on_startup(dp: Dispatcher) -> None:
    setup_middlewares(dp)
    register_view(dp)
    asyncio.create_task(run_schedule_jobs())


async def on_shutdown(_) -> None:
    close_all_sessions()


def main():
    abs_path = Path().absolute()

    logger.add(
        abs_path / 'logs' / 'logs.log',
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} {level:<7} {message}",
        level='DEBUG',
        rotation="00:00",
        compression="zip",
        # serialize=True
    )

    global_init(Config.DATABASE_PATH)

    bot = Bot(token=Config.BOT_TOKEN, parse_mode='markdown')
    dp = Dispatcher(bot=bot, storage=MemoryStorage())

    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        timeout=Config.TIMEOUT,
        relax=Config.RELAX,
    )


if __name__ == '__main__':
    logger.info('Запуск бота...')
    main()
    logger.info('Выключение бота')
