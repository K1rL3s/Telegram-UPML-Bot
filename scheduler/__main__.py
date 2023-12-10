import asyncio
import contextlib

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from sqlalchemy.orm import close_all_sessions

from bot.database import database_init
from bot.settings import get_settings
from bot.setup import configure_logs, make_bot
from scheduler.tasks import add_schedule_jobs


async def main() -> None:
    """Регистратор и запускатор действий по расписанию."""
    configure_logs()
    settings = get_settings()
    session_maker = await database_init(settings.db)
    scheduler = AsyncIOScheduler()

    bot = await make_bot(settings.bot.token)
    async with bot.context():
        add_schedule_jobs(scheduler, bot, session_maker, settings.other.timeout)
        scheduler.start()

        user = await bot.me()
        logger.info(
            "Start schedule for bot @{username} id={id} - '{full_name}'",
            username=user.username,
            id=user.id,
            full_name=user.full_name,
        )

        try:
            while True:
                await asyncio.sleep(5)
        finally:
            scheduler.shutdown()
            close_all_sessions()

            logger.info(
                "Stop schedule for bot @{username} id={id} - '{full_name}'",
                username=user.username,
                id=user.id,
                full_name=user.full_name,
            )


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
