import asyncio
from pathlib import Path

from sqlalchemy.orm import close_all_sessions
from loguru import logger

from bot.database.db_session import database_init
from bot.factory import make_bot, make_dispatcher
from bot.schedule import run_schedule_jobs
from bot.config import Config


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

    bot = await make_bot()
    dp = make_dispatcher()
    dp.shutdown.register(on_shutdown)

    asyncio.create_task(run_schedule_jobs(bot))

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
