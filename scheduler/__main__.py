import asyncio
import contextlib

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from aiogram.enums import ParseMode
from loguru import logger
from sqlalchemy.orm import close_all_sessions

from bot.database import database_init
from bot.settings import get_settings
from bot.setup import setup_logs
from scheduler.tasks import add_schedule_jobs


async def main() -> None:
    """Регистратор и запускатор действий по расписанию."""
    setup_logs()
    settings = get_settings()
    session_maker = await database_init(settings.db)
    scheduler = AsyncIOScheduler()

    async with Bot(
        token=settings.bot.token,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    ).context() as bot:
        bot: "Bot"
        add_schedule_jobs(scheduler, bot, session_maker)
        scheduler.start()

        user = await bot.me()
        logger.info(
            "Start schedule for bot @{username} id={id} - '{full_name}'",
            username=user.username,
            id=user.id,
            full_name=user.full_name,
        )

        await scheduler.start()
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
