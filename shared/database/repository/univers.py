from sqlalchemy import select

from shared.database.models import Univer
from shared.database.repository.base_repo import BaseRepository


class UniverRepository(BaseRepository):
    async def get_cities(self) -> list[str]:
        return await self.select_query_to_list(
            select(Univer.city).distinct().order_by(Univer.city)
        )

    async def get_univers_by_city(self, city: str) -> list[Univer]:
        return await self.select_query_to_list(
            select(Univer).where(Univer.city == city).order_by(Univer.title)
        )

    async def get_univer_by_id(self, univer_id: int) -> Univer:
        return await self._session.scalar(select(Univer).where(Univer.id == univer_id))

    async def add_univer(self, title: str, city: str, description: str) -> Univer:
        univer = Univer(title=title, city=city, description=description)
        self._session.add(univer)
        await self._session.flush()
        return univer
