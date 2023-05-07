import os

from dotenv import load_dotenv
from httpx import AsyncClient


load_dotenv()


class Config:
    BOT_TOKEN = os.environ["BOT_TOKEN"]
    DATABASE_PATH = 'src/database/db_files/database.sqlite?check_same_thread=False'  # noqa
    TIMEOUT = 30
    async_session = AsyncClient(timeout=TIMEOUT)


class CallbackData:
    OPEN_MAIN_MENU = 'open_main_menu'

    OPEN_TODAY_CAFE_MENU = 'open_today_cafe_menu'
    OPEN_CAFE_MENU_ON_ = 'open_cafe_menu_on_'

