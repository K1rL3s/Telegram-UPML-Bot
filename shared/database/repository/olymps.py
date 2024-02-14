from sqlalchemy import delete, select

from shared.database.models import Olymp
from shared.database.repository.base_repo import BaseRepository


class OlympRepository(BaseRepository):
    async def get_subjects(self) -> list[str]:
        return await self.select_query_to_list(
            select(Olymp.subject).distinct().order_by(Olymp.subject)
        )

    async def get_by_subject(self, subject: str) -> list[Olymp]:
        return await self.select_query_to_list(
            select(Olymp).where(Olymp.subject == subject).order_by(Olymp.title)
        )

    async def get_by_id(self, olymp_id: int) -> Olymp:
        return await self._session.scalar(select(Olymp).where(Olymp.id == olymp_id))

    async def add(self, title: str, subject: str, description: str) -> Olymp:
        olymp = Olymp(title=title, subject=subject, description=description)
        self._session.add(olymp)
        await self._session.flush()
        return olymp

    async def delete(self, olymp_id: int) -> None:
        await self._session.execute(delete(Olymp).where(Olymp.id == olymp_id))
        await self._session.flush()
