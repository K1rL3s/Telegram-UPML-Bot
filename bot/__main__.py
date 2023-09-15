import asyncio
import contextlib

from loguru import logger

from bot.database import database_init
from bot.middlewares import setup_middlewares
from bot.setup import make_bot, make_dispatcher, setup_logs
from bot.schedule import run_schedule_jobs
from bot.settings import get_settings


"""На будущее:
1. Накинуть фильтр IsAdmin (и подобные) на роутеры вместо обработчиков
и сделать в фильтре RoleAccess временный кэш.
2. Переделать сохранение юзеров, ибо фильтром SaveUpdateUser выглядит кринжово.
3. Нормально назвать функции загрузки расписаний по фото и остальные функции тоже.
3.1 Нормально назвать переменные там, где плохо названо xd.
3.2 Вынести обработку фото расписаний в отдельный поток с помощью докера.
4. Сделать загрузку картинок/файлов на меню с элективами.
5. Проверить и исправить, что слои database – logic – view сильно не перемешаны.
6. Использовать Callback фабрики.
7. Сделать удаление расписаний уроков.
8. Сделать редис.
"""


async def main() -> None:
    """И поехали! :)."""
    setup_logs()
    settings = get_settings()

    session_maker = await database_init(settings.db)

    bot = await make_bot(settings.bot.BOT_TOKEN)
    dp = make_dispatcher(settings, session_maker)

    setup_middlewares(bot, dp, session_maker)

    asyncio.create_task(run_schedule_jobs(bot, session_maker, settings.other.TIMEOUT))

    logger.info("Запуск пулинга...")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        polling_timeout=settings.other.TIMEOUT,
        allowed_updates=dp.resolve_used_update_types(),
    )

    logger.info("Бот выключен")


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
