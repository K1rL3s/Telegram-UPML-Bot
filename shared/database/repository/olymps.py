from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database.models import Olymp
from shared.database.repository.base_repo import BaseRepository


class OlympRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_subjects(self) -> list[str]:
        return await self.select_query_to_list(
            select(Olymp.subject).distinct().order_by(Olymp.subject.asc())
        )

    async def get_olymps_by_subject(self, subject: str) -> list[Olymp]:
        return await self.select_query_to_list(
            select(Olymp).where(Olymp.subject == subject).order_by(Olymp.title)
        )

    async def get_olymp_by_id(self, olymp_id: int) -> Olymp:
        return await self._session.scalar(select(Olymp).where(Olymp.id == olymp_id))

    async def add_olymp(self, name: str, subject: str, description: str) -> Olymp:
        olymp = Olymp(name=name, subject=subject, description=description)
        self._session.add(olymp)
        await self._session.flush()
        return olymp
