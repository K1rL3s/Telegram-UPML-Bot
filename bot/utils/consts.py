from enum import Enum
from typing import Final


# Переводы всякого
CAFE_MENU_ENG_TO_RU: Final[dict[str, str]] = {
    "breakfast": "завтрак",
    "lunch": "второй завтрак",
    "dinner": "обед",
    "snack": "полдник",
    "supper": "ужин",
}
NOTIFIES_ENG_TO_RU: Final[dict[str, str]] = {
    "all": "всем",
    "grade_10": "десятикам",
    "grade_11": "одиннадцатым",
}
LAUNDRY_ENG_TO_RU: Final[dict[str, str]] = {
    "washing_time": "время стирки",
    "drying_time": "время сушки",
}


class SlashCommands(str, Enum):
    START: str = "start"
    HELP: str = "help"
    SETTINGS: str = "settings"
    MENU: str = "menu"
    LESSONS: str = "lessons"
    CAFE: str = "cafe"
    LAUNDRY: str = "laundry"
    ELECTIVES: str = "electives"
    EDUCATORS: str = "educators"
    CANCEL: str = "cancel"
    STOP: str = "stop"


class TextCommands(str, Enum):
    START: str = "Старт"
    HELP: str = "Помощь"
    SETTINGS: str = "⚙️Настройки"
    MENU: str = "Меню"
    LESSONS: str = "📓Уроки"
    CAFE: str = "🍴Меню"
    LAUNDRY: str = "💦Прачечная"
    ELECTIVES: str = "📖Элективы"
    EDUCATORS: str = "👩‍✈️Воспитатели"
    ADMIN_PANEL: str = "❗Админ панель"
    CANCEL: str = "Отмена"
    STOP: str = CANCEL


class UserCallback(str, Enum):
    OPEN_MAIN_MENU = "open_main_menu"
    OPEN_SETTINGS = "open_settings"
    OPEN_LAUNDRY = "open_laundry"
    OPEN_EDUCATORS = "open_educators"
    OPEN_ELECTIVES = "open_electives"
    OPEN_CAFE_MENU_ON_ = "open_cafe_menu_on_"
    OPEN_CAFE_MENU_TODAY = OPEN_CAFE_MENU_ON_ + "today"
    OPEN_LESSONS_ON_ = "open_lessons_on_"
    OPEN_LESSONS_TODAY = OPEN_LESSONS_ON_ + "today"
    OPEN_EDUCATORS_ON_ = "open_educators_on_"
    OPEN_EDUCATORS_TODAY = OPEN_EDUCATORS_ON_ + "today"

    CHANGE_GRADE_TO_ = "change_grade_to_"
    PREFIX_SWITCH = "switch_"
    SWITCH_LESSONS_NOTIFY = PREFIX_SWITCH + "lessons_notify"
    SWITCH_NEWS_NOTIFY = PREFIX_SWITCH + "news_notify"
    EDIT_SETTINGS_PREFIX = "edit_settings_"
    EDIT_WASHING_TIME = EDIT_SETTINGS_PREFIX + "washing_time"
    EDIT_DRYING_TIME = EDIT_SETTINGS_PREFIX + "drying_time"

    START_LAUNDRY_PREFIX = "start_laundry_"
    START_WASHING_TIMER = START_LAUNDRY_PREFIX + "washing_time"
    START_DRYING_TIMER = START_LAUNDRY_PREFIX + "drying_time"
    CANCEL_LAUNDRY_TIMER = "cancel_laundry_timer"

    CANCEL_STATE = "cancel_state"


class AdminCallback(str, Enum):
    OPEN_ADMIN_PANEL = "open_admin_panel"

    AUTO_UPDATE_CAFE_MENU = "auto_update_cafe_menu"
    EDIT_CAFE_MENU = "edit_cafe_menu"
    EDIT_BREAKFAST = "edit_breakfast"
    EDIT_LUNCH = "edit_lunch"
    EDIT_DINNER = "edit_dinner"
    EDIT_SNACK = "edit_snack"
    EDIT_SUPPER = "edit_supper"
    EDIT_EDUCATORS = "edit_educators"

    UPLOAD_LESSONS = "upload_lessons"

    DO_A_NOTIFY_FOR_ = "do_a_notify_for_"
    NOTIFY_FOR_ALL = DO_A_NOTIFY_FOR_ + "all"
    NOTIFY_FOR_GRADE = DO_A_NOTIFY_FOR_ + "grade"
    NOTIFY_FOR_CLASS = DO_A_NOTIFY_FOR_ + "class"

    OPEN_ADMINS_LIST_PAGE_ = "open_admins_list_page_"
    CHECK_ADMIN_ = "check_admin_"
    REMOVE_ADMIN_ = "remove_admin_"
    REMOVE_ADMIN_SURE_ = REMOVE_ADMIN_ + "sure_"
    ADD_NEW_ADMIN = "add_new_admin"
    ADD_NEW_ADMIN_SURE = "add_new_admin_sure"

    CONFIRM = "confirm_state"


class Roles(str, Enum):
    SUPERADMIN: str = "superadmin"
    ADMIN: str = "admin"


GRADES: Final[tuple[str, ...]] = tuple(
    f"{grade}{letter}" for grade in (range(10, 11 + 1)) for letter in "АБВ"
)
LAUNDRY_REPEAT: Final[int] = 30  # Повтор таймера прачки через 30 минут
NO_DATA: Final[str] = "Н/д"

SLASH_COMMANDS: Final[dict[str, str]] = {
    SlashCommands.START: "Старт",
    SlashCommands.HELP: "Помощь",
    SlashCommands.SETTINGS: "Настройки",
    SlashCommands.MENU: "Меню",
}
