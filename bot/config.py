import os
from datetime import timedelta, timezone
from typing import Final

from dotenv import load_dotenv
from httpx import AsyncClient


load_dotenv()


class Config:
    BOT_TOKEN: Final[str] = os.getenv("BOT_TOKEN")
    TESSERACT_PATH: Final[str] = os.getenv("TESSERACT_PATH")
    TIMEOUT: Final[int] = 30
    TIMEZONE: Final[timezone] = timezone(
        timedelta(hours=int(os.getenv("TIMEZONE") or 0))
    )
    async_session: Final[AsyncClient] = AsyncClient(timeout=TIMEOUT)

    POSTGRES_HOST: Final[str] = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = (
        int(os.getenv('POSTGRES_DOCKER_PORT'))
        if POSTGRES_HOST == 'database' else
        int(os.getenv('POSTGRES_HOST_PORT'))
    )
    POSTGRES_DB: Final[str] = os.getenv("POSTGRES_DB")
    POSTGRES_USER: Final[str] = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: Final[str] = os.getenv("POSTGRES_PASSWORD")
