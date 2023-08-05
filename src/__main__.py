import asyncio
from pathlib import Path

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.orm import close_all_sessions
from loguru import logger

from src.database.db_session import global_init
from src.schedule import run_schedule_jobs
from src.utils.consts import Config
from src.view import register_view_routers
from src.middlewares import setup_middlewares


def on_startup(dp: Dispatcher) -> None:
    setup_middlewares(dp)
    register_view_routers(dp)
    asyncio.create_task(run_schedule_jobs())


async def on_shutdown() -> None:
    close_all_sessions()


# Тодо: Починить клавиатуры :)
async def main():
    abs_path = Path().absolute()

    logger.add(
        abs_path / 'database' / 'db_files' / 'logs.log',
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} {level:<7} {message}",
        level='DEBUG',
        rotation="00:00",
        compression="zip",
        # serialize=True
    )

    global_init(Config.DATABASE_PATH)

    bot = Bot(token=Config.BOT_TOKEN, parse_mode='markdown')
    dp = Dispatcher(bot=bot, storage=MemoryStorage())
    on_startup(dp)
    dp.shutdown.register(on_shutdown)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        polling_timeout=Config.TIMEOUT,
        allowed_updates=dp.resolve_used_update_types()
    )


if __name__ == '__main__':
    logger.info('Запуск бота...')
    asyncio.set_event_loop(asyncio.new_event_loop())
    asyncio.run(main())
    logger.info('Выключение бота')
