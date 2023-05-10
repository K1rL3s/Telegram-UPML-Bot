import os
from enum import Enum

from dotenv import load_dotenv
from httpx import AsyncClient


load_dotenv()


class Config:
    BOT_TOKEN = os.environ["BOT_TOKEN"]
    DATABASE_PATH = 'src/database/db_files/database.sqlite?check_same_thread=False'  # noqa
    TESSERACT_PATH = os.environ["TESSERACT_PATH"]
    TIMEOUT = 60
    RELAX = 0.5
    async_session = AsyncClient(timeout=TIMEOUT)


class CallbackData:
    OPEN_MAIN_MENU = 'open_main_menu'
    OPEN_SETTINGS = 'open_settings'
    OPEN_ADMIN_MENU = 'open_admin_menu'
    OPEN_CAFE_MENU_ON_ = 'open_cafe_menu_on_'
    OPEN_CAFE_MENU_TODAY = OPEN_CAFE_MENU_ON_ + 'today'
    OPEN_LESSONS_ON_ = 'open_lessons_on_'
    OPEN_LESSONS_TODAY = OPEN_LESSONS_ON_ + 'today'

    CHANGE_GRADE_TO_ = 'edit_grade_to_'
    PREFIX_SWITCH = 'switch_'
    SWITCH_LESSONS_NOTIFY = PREFIX_SWITCH + 'lessons_notify'
    SWITCH_NEWS_NOTIFY = PREFIX_SWITCH + 'news_notify'

    CANCEL_STATE = 'cancel_state'

    AUTO_UPDATE_CAFE_MENU = 'auto_update_cafe_menu'
    MANUAL_UPDATE_CAFE_MENU = 'manual_update_cafe_menu'
    UPLOAD_LESSONS = 'upload_lessons'
    DO_A_NOTIFY_FOR_ = 'do_a_notify_for_'

    OPEN_ADMINS_LIST_PAGE_ = 'open_admins_list_page_'
    CHECK_ADMIN_ = 'check_admin_'
    REMOVE_ADMIN_ = 'remove_admin_'
    REMOVE_ADMIN_SURE_ = 'remove_admin_sure_'
    ADD_NEW_ADMIN = 'add_new_admin'
    ADD_NEW_ADMIN_SURE = 'add_new_admin_sure'


class Roles(Enum):
    SUPERADMIN = 'superadmin'
    ADMIN = 'admin'


GRADES = tuple(
    f'{grade}{letter}' for grade in (range(10, 11 + 1)) for letter in 'АБВ'
)

