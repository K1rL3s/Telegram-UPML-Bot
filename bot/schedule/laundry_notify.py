from datetime import timedelta

from aiogram import Bot

from bot.database.db_funcs import Repository
from bot.database.db_session import get_session
from bot.funcs.laundry import laundry_cancel_timer_func
from bot.keyboards import laundry_keyboard
from bot.utils.consts import LAUNDRY_REPEAT
from bot.utils.datehelp import datetime_now
from bot.utils.funcs import one_notify


async def check_laundry_timers(bot: Bot) -> None:
    """
    Делатель уведомлений для истёкших таймеров прачки.
    """
    async with get_session() as session:
        repo = Repository(session)
        for laundry in await repo.get_expired_laundries():
            laundry.rings = laundry.rings or 0

            result = await one_notify(
                bot,
                repo,
                laundry.user,
                f'🔔Таймер прачечной вышел! ({laundry.rings + 1})',
                await laundry_keyboard(laundry, laundry.rings < 2)
            )
            if not result:
                continue

            if laundry.rings >= 2:
                await laundry_cancel_timer_func(laundry.user.user_id)
            else:
                now = datetime_now()
                await repo.save_or_update_laundry(
                    laundry.user.user_id,
                    rings=laundry.rings + 1, start_time=now,
                    end_time=now + timedelta(minutes=LAUNDRY_REPEAT)
                )
