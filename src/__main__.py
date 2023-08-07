import asyncio
from pathlib import Path

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from sqlalchemy.orm import close_all_sessions
from loguru import logger

from src.database.db_session import database_init
from src.schedule import run_schedule_jobs
from src.utils.consts import Config, bot_commands
from src.view import register_view_routers
from src.middlewares import setup_middlewares


async def set_commands(bot: Bot) -> bool:
    return await bot.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in bot_commands.items()
        ],
        language_code='ru'
    )


async def on_shutdown() -> None:
    close_all_sessions()


async def main():
    logger.info('Запуск бота...')

    workdir_path = Path(__file__).parent.parent.absolute()

    logger.add(
        workdir_path / 'logs' / 'logs.log',
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} {level:<7} {message}",
        level='DEBUG',
        rotation="00:00",
        compression="zip",
    )

    await database_init()

    bot = Bot(token=Config.BOT_TOKEN, parse_mode='markdown')
    dp = Dispatcher(storage=MemoryStorage())

    await set_commands(bot)
    setup_middlewares(dp)
    register_view_routers(dp)
    asyncio.create_task(run_schedule_jobs(bot))

    dp.shutdown.register(on_shutdown)

    logger.info('Запуск пулинга...')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        polling_timeout=Config.TIMEOUT,
        allowed_updates=dp.resolve_used_update_types()
    )
    logger.info('Выключение бота')


if __name__ == '__main__':
    asyncio.run(main())
