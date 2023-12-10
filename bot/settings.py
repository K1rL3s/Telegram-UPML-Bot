import os
from pathlib import Path
from typing import Optional, Union

from dotenv import load_dotenv
from pydantic import BaseModel


class DBSettings(BaseModel):
    """Настройки подключения к базе данных."""

    host: str
    host_port: int
    db: str
    user: str
    password: str


class RedisSettings(BaseModel):
    """Настройки редиса."""

    host: str
    host_port: int
    password: str


class BotSettings(BaseModel):
    """Настройки телеграм-бота."""

    token: str


class OtherSettings(BaseModel):
    """Общие настройки проекта."""

    tesseract_path: str
    timeout: int
    timezone_offset: int


class Settings(BaseModel):
    """Сборник настроек :)."""

    db: DBSettings
    redis: RedisSettings
    bot: BotSettings
    other: OtherSettings


def get_settings(dotenv_path: "Optional[Union[Path, str]]" = None) -> Settings:
    """
    Создание настроек из переменных среды.

    :param dotenv_path: Путь до .env файла. Используется для alembic'а.
    :return: Настройки.
    """
    if dotenv_path:
        load_dotenv(dotenv_path)

    db = DBSettings(
        host=os.environ["POSTGRES_HOST"],
        host_port=int(os.environ["POSTGRES_HOST_PORT"]),
        db=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )
    redis = RedisSettings(
        host=os.environ["REDIS_HOST"],
        host_port=int(os.environ["REDIS_HOST_PORT"]),
        password=os.environ["REDIS_PASSWORD"],
    )
    bot = BotSettings(
        token=os.environ["BOT_TOKEN"],
    )
    other = OtherSettings(
        tesseract_path=os.environ["TESSERACT_PATH"],
        timeout=int(os.getenv("TIMEOUT") or 10),
        timezone_offset=int(os.getenv("TIMEZONE_OFFSET") or 0),
    )

    return Settings(db=db, redis=redis, bot=bot, other=other)
