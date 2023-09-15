from typing import TYPE_CHECKING

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from bot.database.base import AlchemyBaseModel

if TYPE_CHECKING:
    from bot.settings import DBSettings


__all__ = (
    "AlchemyBaseModel",
    "database_init",
)


async def database_init(db_settings: "DBSettings") -> async_sessionmaker[AsyncSession]:
    """Иницализация подключения к базе данных."""
    database_url = URL.create(
        drivername="postgresql+asyncpg",
        username=db_settings.POSTGRES_USER,
        password=db_settings.POSTGRES_PASSWORD,
        host=db_settings.POSTGRES_HOST,
        port=db_settings.POSTGRES_HOST_PORT,
        database=db_settings.POSTGRES_DB,
    )
    async_engine = create_async_engine(database_url)

    return async_sessionmaker(
        bind=async_engine,
        autoflush=False,
        future=True,
        expire_on_commit=False,
    )
