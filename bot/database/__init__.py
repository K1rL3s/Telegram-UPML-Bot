from typing import TYPE_CHECKING

from sqlalchemy import MetaData, URL
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase

if TYPE_CHECKING:
    from bot.settings import DBSettings


__all__ = (
    "SqlAlchemyBase",
    "database_init",
)


class SqlAlchemyBase(DeclarativeBase):
    """Декларативная база для моделей Алхимии."""

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        },
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
