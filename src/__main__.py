from pathlib import Path

from aiogram import Dispatcher, Bot, executor
from loguru import logger
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from src.utils.consts import Config
from src.view import register_view
from src.middlewares import setup_middlewares


async def on_startup(dp: Dispatcher) -> None:
    setup_middlewares(dp)
    register_view(dp)


async def on_shutdown(_) -> None:
    pass


def main():
    abs_path = Path().absolute().parent

    logger.add(
        abs_path / 'logs' / 'logs.log',
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} {level:<7} {message}",
        level='DEBUG',
        rotation="00:00",
        compression="zip",
        # serialize=True
    )

    bot = Bot(token=Config.BOT_TOKEN)
    dp = Dispatcher(bot=bot, storage=MemoryStorage())

    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        timeout=Config.TIMEOUT
    )


if __name__ == '__main__':
    logger.info('Запуск бота...')
    main()
    logger.info('Выключение бота')
