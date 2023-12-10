from typing import TYPE_CHECKING

from scheduler.tasks.laundry_notify import check_laundry_timers
from scheduler.tasks.update_cafe_menu import update_cafe_menu
from scheduler.tasks.update_educators import update_educators

if TYPE_CHECKING:
    from aiogram import Bot
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


__all__ = ("add_schedule_jobs",)


def add_schedule_jobs(
    scheduler: "AsyncIOScheduler",
    bot: "Bot",
    session_maker: "async_sessionmaker[AsyncSession]",
    timeout: int,
) -> None:
    """
    Добавление задач в расписание.

    :param scheduler: Шедулер.
    :param bot: ТГ Бот.
    :param session_maker: Пул сессий.
    :param timeout: Таймаут в ожидании запроса на расписание еды.
    """
    scheduler.add_job(
        update_cafe_menu,
        trigger="cron",
        args=[session_maker, timeout],
        hour="7-16",
    )
    scheduler.add_job(
        check_laundry_timers,
        trigger="cron",
        args=[bot, session_maker],
        minute="*",
        second=0,
    )
    scheduler.add_job(
        update_educators,
        trigger="cron",
        args=[session_maker],
        day="*",
        hour=0,
        minute=0,
        second=0,
    )
