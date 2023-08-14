import asyncio

from loguru import logger

from bot.database.db_session import database_init
from bot.setup import make_bot, make_dispatcher, setup_logs
from bot.schedule import run_schedule_jobs
from bot.config import Config


async def main():
    setup_logs()

    await database_init()

    bot = await make_bot()
    dp = make_dispatcher()

    asyncio.create_task(run_schedule_jobs(bot))

    logger.info('Запуск пулинга...')

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        polling_timeout=Config.TIMEOUT,
        allowed_updates=dp.resolve_used_update_types()
    )

    logger.info('Бот выключен')


if __name__ == '__main__':
    asyncio.run(main())
