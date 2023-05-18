from src.database.db_funcs import get_expired_laundries
from src.handlers.laundry import laundry_cancel_timer_handler
from src.keyboards import laundry_keyboard
from src.utils.funcs import one_notify


async def check_laundry_timers() -> None:
    """
    Делатель уведомлений для истёкших таймеров прачки.
    """
    for laundry in get_expired_laundries():
        result = await one_notify(
            '🔔Таймер прачечной вышел!',
            laundry.user,
            laundry_keyboard(laundry.user.user_id, False)
        )
        if result:
            laundry_cancel_timer_handler(laundry.user.user_id)
