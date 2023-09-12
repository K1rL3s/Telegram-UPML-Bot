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
        POSTGRES_HOST=os.environ["POSTGRES_HOST"],
        POSTGRES_HOST_PORT=int(os.environ["POSTGRES_HOST_PORT"]),
        POSTGRES_DB=os.environ["POSTGRES_DB"],
        POSTGRES_USER=os.environ["POSTGRES_USER"],
        POSTGRES_PASSWORD=os.environ["POSTGRES_PASSWORD"],
    )
    bot = BotSettings(
        BOT_TOKEN=os.environ["BOT_TOKEN"],
    )
    other = OtherSettings(
        TESSERACT_PATH=os.environ["TESSERACT_PATH"],
        TIMEOUT=int(os.getenv("TIMEOUT") or 10),
        TIMEZONE_OFFSET=int(os.getenv("TIMEZONE_OFFSET") or 0),
    )

    return Settings(
        db=db,
        bot=bot,
        other=other,
    )
