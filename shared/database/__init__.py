from typing import TYPE_CHECKING

from loguru import logger
from redis.asyncio.client import Redis
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from shared.database.base import AlchemyBaseModel, UserRelatedModel

if TYPE_CHECKING:
    from shared.core.settings import DBSettings, RedisSettings


__all__ = (
    "AlchemyBaseModel",
    "UserRelatedModel",
    "database_init",
    "redis_init",
)


@logger.catch(reraise=True)
async def database_init(db_settings: "DBSettings") -> async_sessionmaker[AsyncSession]:
    """
    Иницализация подключения к базе данных.

    :param db_settings: Настройки базы данных.
    :return: Асинхронный делатель сессий. :)
    """
    database_url = URL.create(
        drivername="postgresql+asyncpg",
        username=db_settings.user,
        password=db_settings.password,
        host=db_settings.host,
        port=db_settings.host_port,
        database=db_settings.db,
    )
    async_engine = create_async_engine(database_url)

    # Проверка подключения к базе данных
    async with async_engine.begin():
        pass

    return async_sessionmaker(
        bind=async_engine,
        autoflush=False,
        future=True,
        expire_on_commit=False,
    )


@logger.catch(reraise=True)
async def redis_init(redis_settings: "RedisSettings") -> "Redis":
    """
    Создание подключения к редису.

    :param redis_settings: Настройки редиса.
    :return: Редис.
    """
    redis = Redis(
        host=redis_settings.host,
        port=redis_settings.host_port,
        password=redis_settings.password,
    )
    # Проверка подключения к редису
    await redis.ping()

    return redis
