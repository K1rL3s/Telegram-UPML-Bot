import asyncio
import contextlib

from bot.database import database_init, redis_init
from bot.middlewares import setup_global_middlewares
from bot.setup import configure_logs, make_bot, make_dispatcher
from bot.settings import get_settings


"""На будущее:
1. Cделать в фильтре RoleAccess временный кэш (?).
3. Нормально назвать функции загрузки расписаний по фото и остальные функции тоже.
3.1 Нормально назвать переменные там, где плохо названо xd.
3.2 Вынести обработку фото расписаний в отдельный поток с помощью докера.
4. Сделать загрузку картинок/файлов на меню с элективами.
5. Проверить и исправить, что слои database – logic – view сильно не перемешаны.
6. Использовать Callback фабрики.
7. Сделать удаление расписаний уроков.
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
