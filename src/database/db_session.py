import contextlib

import sqlalchemy.ext.declarative as dec
from loguru import logger
from sqlalchemy import URL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker,
    create_async_engine,
)

from src.utils.consts import Config


SqlAlchemyBase = dec.declarative_base()
__factory: async_sessionmaker | None = None


async def database_init() -> None:
    """
    Иницализация подключения к базе данных.
    """

    global __factory

    if __factory:
        return

    DATABASE_URL = URL.create(
        drivername="postgresql+asyncpg",
        username=Config.POSTGRES_USER,
        password=Config.POSTGRES_PASSWORD,
        host=Config.POSTGRES_HOST,
        port=Config.POSTGRES_PORT,
        database=Config.POSTGRES_DB,
    )

    async_engine = create_async_engine(DATABASE_URL)
    __factory = async_sessionmaker(
        bind=async_engine,
        autoflush=False,
        future=True,
        expire_on_commit=False,
    )


@contextlib.asynccontextmanager
async def get_session() -> AsyncSession:
    """
    Создатель сессии для работы с базой данных.

    :return: Сессия SqlAlchemy.
    """
    if not __factory:
        raise RuntimeError("Брат, а кто database_init вызывать будет?")

    try:
        async with __factory() as session:
            yield session
    except SQLAlchemyError as e:
        logger.exception(e)
        raise e
