import os
from typing import Optional, TYPE_CHECKING, Union

from dotenv import load_dotenv

from pydantic import BaseModel

if TYPE_CHECKING:
    from pathlib import Path


class DBSettings(BaseModel):
    """Настройки подключения к базе данных."""

    POSTGRES_HOST: str
    POSTGRES_HOST_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str


class BotSettings(BaseModel):
    """Настройки телеграм-бота."""

    BOT_TOKEN: str


class OtherSettings(BaseModel):
    """Общие настройки проекта."""

    TESSERACT_PATH: str
    TIMEOUT: int
    TIMEZONE_OFFSET: int


class Settings(BaseModel):
    """Сборник настроек :)."""

    db: DBSettings
    bot: BotSettings
    other: OtherSettings


def get_settings(path_to_env: "Optional[Union[str, Path]]" = None) -> Settings:
    """Загрузка переменных из .env и создание настроек.

    :param path_to_env: Путь до .env файла.
    :return: Настройки.
    """
    load_dotenv(path_to_env, override=True)

    db = DBSettings(
        POSTGRES_HOST=os.getenv("POSTGRES_HOST"),
        POSTGRES_HOST_PORT=int(os.getenv("POSTGRES_HOST_PORT")),
        POSTGRES_DB=os.getenv("POSTGRES_DB"),
        POSTGRES_USER=os.getenv("POSTGRES_USER"),
        POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD"),
    )
    bot = BotSettings(
        BOT_TOKEN=os.getenv("BOT_TOKEN"),
    )
    other = OtherSettings(
        TESSERACT_PATH=os.getenv("TESSERACT_PATH"),
        TIMEOUT=20,
        TIMEZONE_OFFSET=int(os.getenv("TIMEZONE_OFFSET") or 0),
    )

    return Settings(
        db=db,
        bot=bot,
        other=other,
    )
