import datetime as dt
from typing import TYPE_CHECKING

from bot.database.repository.repository import Repository
from bot.database.db_session import get_session
from bot.funcs.client.laundry import laundry_cancel_timer_func
from bot.keyboards import laundry_keyboard
from bot.utils.consts import LAUNDRY_REPEAT
from bot.utils.datehelp import datetime_now
from bot.utils.notify import one_notify

if TYPE_CHECKING:
    from aiogram import Bot


async def check_laundry_timers(bot: "Bot") -> None:
    """Делатель уведомлений для истёкших таймеров прачечной."""
    async with get_session() as session:
        repo = Repository(session)
        for laundry in await repo.laundry.get_expired():
            rings = laundry.rings or 0

            result = await one_notify(
                bot,
                repo.user,
                laundry.user,
                f"🔔Таймер прачечной вышел! ({rings + 1})",
                await laundry_keyboard(laundry, rings < 2),
            )
            if not result or rings >= 2:
                await laundry_cancel_timer_func(repo.laundry, laundry.user.user_id)
            else:
                now = datetime_now()
                await repo.laundry.save_or_update_to_db(
                    laundry.user.user_id,
                    rings=rings + 1,
                    start_time=now,
                    end_time=now + dt.timedelta(minutes=LAUNDRY_REPEAT),
                )
