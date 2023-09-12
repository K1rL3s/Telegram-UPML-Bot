from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(ABC):
    """Базовый класс для репозиториев, нужен для переиспользования кода."""

    _session: "AsyncSession"
