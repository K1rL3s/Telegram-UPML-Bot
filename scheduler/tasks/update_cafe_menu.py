from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.database.repository.repository import Repository
from bot.upml.save_cafe_menu import process_cafe_menu


async def update_cafe_menu(
    session_maker: "async_sessionmaker[AsyncSession]",
    timeout: int,
) -> None:
    """Автоматическое обновление расписание столовой, используется в apscheduler."""
    async with session_maker.begin() as session:
        repo = Repository(session)

        if await repo.menu.is_filled_on_today():
            return

        await process_cafe_menu(repo.menu, timeout)
