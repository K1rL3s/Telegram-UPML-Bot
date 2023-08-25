import os
from typing import Final

from dotenv import load_dotenv


load_dotenv()


class DBSettings:
    """Настройки подключения к базе данных."""

    POSTGRES_HOST: Final[str] = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = (
        int(os.getenv("POSTGRES_DOCKER_PORT"))
        if POSTGRES_HOST == "database"
        else int(os.getenv("POSTGRES_HOST_PORT"))
    )
    POSTGRES_DB: Final[str] = os.getenv("POSTGRES_DB")
    POSTGRES_USER: Final[str] = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: Final[str] = os.getenv("POSTGRES_PASSWORD")


class BotSettings:
    """Настройки телеграм-бота."""

    BOT_TOKEN: Final[str] = os.getenv("BOT_TOKEN")


class Settings:
    """Общие настройки проекта."""

    TESSERACT_PATH: Final[str] = os.getenv("TESSERACT_PATH")
    TIMEOUT: Final[int] = 30
    TIMEZONE_OFFSET: Final[int] = int(os.getenv("TIMEZONE") or 0)
