"""
Модуль, в котором хранятся aioschedule задачи.
(Те, которые рассылка в определённое время, обновление меню в начале недели,
 пулинг вк для расписаний уроков)
"""

import asyncio

import aioschedule

from src.schedule.update_cafe_menu import update_cafe_menu


async def run_schedule_jobs() -> None:
    # Каждый час с 7:00 до 16:00 с понедельника по четверг
    # Не работает, исправить
    aioschedule.every().hour.at(":00").do(
        update_cafe_menu
    ).day.at("07:00").to("16:00").monday.to("thursday")

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(5)
