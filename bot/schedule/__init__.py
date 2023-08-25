"""Модуль, в котором хранятся aioschedule задачи.

Те, которые рассылка в определённое время, обновление меню в начале недели,
пулинг вк для расписаний уроков.
"""
import asyncio
from typing import TYPE_CHECKING

import aioschedule

from bot.schedule.laundry_notify import check_laundry_timers
from bot.schedule.update_cafe_menu import update_cafe_menu

if TYPE_CHECKING:
    from aiogram import Bot

__all__ = [
    "run_schedule_jobs",
]


async def run_schedule_jobs(bot: "Bot") -> None:
    """Регистратор и запускатор действий по расписанию."""
    for hour in range(7, 16 + 1):
        aioschedule.every().day.at(f"{hour:0>2}:00").do(update_cafe_menu)
    aioschedule.every().minute.do(check_laundry_timers, bot=bot)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(5)
