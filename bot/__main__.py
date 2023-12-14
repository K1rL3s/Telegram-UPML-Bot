import asyncio
import contextlib

from bot.base import make_bot, make_dispatcher
from bot.middlewares import setup_global_middlewares
from shared.core.log import configure_logs
from shared.core.settings import get_settings
from shared.database import database_init, redis_init

"""На будущее:
1. Cделать в фильтре RoleAccess временный кэш (?).
3.1 Нормально назвать переменные там, где плохо названо xd.
3.2 Вынести обработку фото расписаний в отдельный поток с помощью докера.
4. Сделать загрузку картинок/файлов на меню с элективами.
5. Проверить и исправить, что слои database – logic – view сильно не перемешаны.
7. Сделать удаление расписаний уроков.
8. Решить проблему с добавлением новых ролей в бд.
"""


async def main() -> None:
    """И поехали! :)."""
    configure_logs()

    settings = get_settings()
    redis = await redis_init(settings.redis)
    session_maker = await database_init(settings.db)

    bot = await make_bot(settings.bot.token)
    dp = make_dispatcher(settings, redis)

    setup_global_middlewares(bot, dp, session_maker)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        polling_timeout=settings.other.timeout,
        allowed_updates=dp.resolve_used_update_types(),
    )


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
