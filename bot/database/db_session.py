import contextlib
from collections.abc import AsyncIterator

from loguru import logger
from sqlalchemy import MetaData, URL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from bot.settings import DBSettings


class SqlAlchemyBase(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


__factory: async_sessionmaker[AsyncSession] | None = None


async def database_init() -> None:
    """
    Иницализация подключения к базе данных.
    """

    global __factory

    if __factory:
        return

    database_url = URL.create(
        drivername="postgresql+asyncpg",
        username=DBSettings.POSTGRES_USER,
        password=DBSettings.POSTGRES_PASSWORD,
        host=DBSettings.POSTGRES_HOST,
        port=DBSettings.POSTGRES_PORT,
        database=DBSettings.POSTGRES_DB,
    )

    async_engine = create_async_engine(database_url)
    __factory = async_sessionmaker(
        bind=async_engine,
        autoflush=False,
        future=True,
        expire_on_commit=False,
    )


@contextlib.asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    """
    Создатель сессии для работы с базой данных.

    :return: Асинхронная сессия SqlAlchemy.
    """
    if not __factory:
        raise RuntimeError("Брат, а кто database_init вызывать будет?")

    try:
        async with __factory() as session:
            yield session
    except SQLAlchemyError as e:
        logger.exception(e)
        raise e
