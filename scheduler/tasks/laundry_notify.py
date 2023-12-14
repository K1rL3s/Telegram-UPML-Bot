import datetime as dt
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.keyboards import laundry_keyboard
from shared.database.repository.repository import Repository
from shared.utils.consts import REPEAT_LAUNDRY_TIMER
from shared.utils.datehelp import datetime_now
from shared.utils.notify import do_one_notify

if TYPE_CHECKING:
    from aiogram import Bot

    from shared.database.models import Laundry
    from shared.database.repository import LaundryRepository


LAUNDRY_TIMER_EXPIRED = "🔔Таймер прачечной вышел! ({0})".format


async def check_laundry_timers(
    bot: "Bot",
    session_maker: "async_sessionmaker[AsyncSession]",
) -> None:
    """Обход всех истёкших таймеров прачечной."""
    async with session_maker.begin() as session:
        repo = Repository(session)
        for laundry in await repo.laundry.get_expired():
            await check_expired_timer(bot, laundry, repo)


async def check_expired_timer(
    bot: "Bot",
    laundry: "Laundry",
    repo: "Repository",
) -> None:
    """Делатель уведомления для истёкшего таймера."""
    rings = laundry.rings or 0
    is_last_call = rings < 2
    is_notify_sent = await do_one_notify(
        LAUNDRY_TIMER_EXPIRED(rings + 1),
        bot,
        repo.user,
        laundry.user,
        await laundry_keyboard(laundry, is_last_call),
    )

    if rings >= 2 or not is_notify_sent:
        await repo.laundry.cancel_timer(laundry.user_id)
    else:
        await increment_timer(rings, laundry, repo.laundry)


async def increment_timer(
    rings: int,
    laundry: "Laundry",
    repo: "LaundryRepository",
) -> None:
    """Переносит таймер на REPEAT_LAUNDRY_TIMER минут вперёд после уведомления."""
    now = datetime_now()
    end_time = now + dt.timedelta(minutes=REPEAT_LAUNDRY_TIMER)

    await repo.save_or_update_to_db(
        laundry.user.user_id,
        rings=rings + 1,
        start_time=now,
        end_time=end_time.replace(second=0, microsecond=0),  # Обнуление секунд
    )
