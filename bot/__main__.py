import asyncio
import contextlib

from loguru import logger

from bot.database import database_init, redis_init
from bot.middlewares import setup_global_middlewares
from bot.setup import make_bot, make_dispatcher, setup_logs
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
    setup_logs()
    settings = get_settings()

    session_maker = await database_init(settings.db)
    redis = await redis_init(settings.redis)

    bot = await make_bot(settings.bot.token)
    dp = make_dispatcher(settings, session_maker, redis)

    setup_global_middlewares(bot, dp, session_maker)

    user = await bot.me()  # Copypaste from aiogram
    logger.info(
        "Start polling for bot @{username} id={id} - '{full_name}'",
        username=user.username,
        id=user.id,
        full_name=user.full_name,
    )  # Copypaste from aiogram

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        polling_timeout=settings.other.timeout,
        allowed_updates=dp.resolve_used_update_types(),
    )

    logger.info(
        "Stop polling for bot @{username} id={id} - '{full_name}'",
        username=user.username,
        id=user.id,
        full_name=user.full_name,
    )


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
