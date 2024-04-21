from abc import ABC
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from sqlalchemy import Select
    from sqlalchemy.ext.asyncio import AsyncSession


T = TypeVar("T")


class BaseRepository(ABC):
    """Базовый класс для репозиториев, нужен для переиспользования кода."""

    _session: "AsyncSession"

    def __init__(self, session: "AsyncSession") -> None:
        self._session = session

    async def select_query_to_list(self, query: "Select[tuple[T]]") -> list[T]:
        return list((await self._session.scalars(query)).all())
