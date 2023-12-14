from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from shared.database.repository.repository import Repository
from shared.upml.educators_excel import load_educators_from_xlsx


async def update_educators(session_maker: "async_sessionmaker[AsyncSession]") -> None:
    """Автоматическое обновление расписаний воспитателей из экселя."""
    async with session_maker.begin() as session:
        repo = Repository(session)
        await load_educators_from_xlsx(repo.educators)
