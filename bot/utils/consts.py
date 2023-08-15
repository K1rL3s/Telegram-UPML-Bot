from enum import Enum
from typing import Final


# Переводы всякого
menu_eng_to_ru: Final[dict[str, str]] = {
    'breakfast': 'завтрак',
    'lunch': 'второй завтрак',
    'dinner': 'обед',
    'snack': 'полдник',
    'supper': 'ужин'
}
notifies_eng_to_ru: Final[dict[str, str]] = {
    'all': 'всем',
    'grade_10': 'десятикам',
    'grade_11': 'одиннадцатым',
}
times_eng_to_ru: Final[dict[str, str]] = {
    'washing_time': 'время стирки',
    'drying_time': 'время сушки'
}


class SlashCommands:
    START: Final[str] = 'start'
    HELP: Final[str] = 'help'
    SETTINGS: Final[str] = 'settings'
    MENU: Final[str] = 'menu'
    LESSONS: Final[str] = 'lessons'
    CAFE: Final[str] = 'cafe'
    LAUNDRY: Final[str] = 'laundry'
    ELECTIVES: Final[str] = 'electives'
    EDUCATORS: Final[str] = 'educators'
    CANCEL: Final[str] = 'cancel'
    STOP: Final[str] = 'stop'


class TextCommands:
    START: Final[str] = 'Старт'
    HELP: Final[str] = 'Помощь'
    SETTINGS: Final[str] = 'Настройки'
    MENU: Final[str] = 'Меню'
    LESSONS: Final[str] = 'Уроки'
    CAFE: Final[str] = 'Столовая'
    LAUNDRY: Final[str] = 'Прачечная'
    ELECTIVES: Final[str] = 'Элективы'
    EDUCATORS: Final[str] = 'Воспитатели'
    CANCEL: Final[str] = 'Отмена'
    STOP: Final[str] = 'Отмена'


class CallbackData:
    OPEN_MAIN_MENU = 'open_main_menu'
    OPEN_SETTINGS = 'open_settings'
    OPEN_LAUNDRY = 'open_laundry'
    OPEN_EDUCATORS = 'open_educators'
    OPEN_ELECTIVES = 'open_electives'
    OPEN_ADMIN_PANEL = 'open_admin_panel'
    OPEN_CAFE_MENU_ON_ = 'open_cafe_menu_on_'
    OPEN_CAFE_MENU_TODAY = OPEN_CAFE_MENU_ON_ + 'today'
    OPEN_LESSONS_ON_ = 'open_lessons_on_'
    OPEN_LESSONS_TODAY = OPEN_LESSONS_ON_ + 'today'
    OPEN_EDUCATORS_ON_ = 'open_educators_on_'
    OPEN_EDUCATORS_TODAY = 'open_educators_on_' + 'today'

    CHANGE_GRADE_TO_ = 'edit_grade_to_'
    PREFIX_SWITCH = 'switch_'
    SWITCH_LESSONS_NOTIFY = PREFIX_SWITCH + 'lessons_notify'
    SWITCH_NEWS_NOTIFY = PREFIX_SWITCH + 'news_notify'
    EDIT_SETTINGS_PREFIX = 'edit_settings_'
    EDIT_WASHING_TIME = EDIT_SETTINGS_PREFIX + 'washing_time'
    EDIT_DRYING_TIME = EDIT_SETTINGS_PREFIX + 'drying_time'

    CANCEL_STATE = 'cancel_state'
    CONFIRM = 'confirm_state'

    AUTO_UPDATE_CAFE_MENU = 'auto_update_cafe_menu'
    EDIT_CAFE_MENU = 'edit_cafe_menu'
    EDIT_BREAKFAST = 'edit_breakfast'
    EDIT_LUNCH = 'edit_lunch'
    EDIT_DINNER = 'edit_dinner'
    EDIT_SNACK = 'edit_snack'
    EDIT_SUPPER = 'edit_supper'

    EDIT_EDUCATORS = 'edit_educators'

    UPLOAD_LESSONS = 'upload_lessons'

    DO_A_NOTIFY_FOR_ = 'do_a_notify_for_'
    NOTIFY_FOR_ALL = DO_A_NOTIFY_FOR_ + 'all'
    NOTIFY_FOR_GRADE = DO_A_NOTIFY_FOR_ + 'grade'
    NOTIFY_FOR_CLASS = DO_A_NOTIFY_FOR_ + 'class'

    OPEN_ADMINS_LIST_PAGE_ = 'open_admins_list_page_'
    CHECK_ADMIN_ = 'check_admin_'
    REMOVE_ADMIN_ = 'remove_admin_'
    REMOVE_ADMIN_SURE_ = REMOVE_ADMIN_ + 'sure_'
    ADD_NEW_ADMIN = 'add_new_admin'
    ADD_NEW_ADMIN_SURE = 'add_new_admin_sure'

    START_LAUNDRY_PREFIX = 'start_laundry_'
    START_WASHING_TIMER = START_LAUNDRY_PREFIX + 'washing_time'
    START_DRYING_TIMER = START_LAUNDRY_PREFIX + 'drying_time'
    CANCEL_LAUNDRY_TIMER = 'cancel_laundry_timer'


class Roles(Enum):
    SUPERADMIN: Final[str] = 'superadmin'
    ADMIN: Final[str] = 'admin'


GRADES: Final[tuple[str, ...]] = tuple(
    f'{grade}{letter}'
    for grade in (range(10, 11 + 1))
    for letter in 'АБВ'
)
LAUNDRY_REPEAT: Final[int] = 30  # Повтор таймера прачки через 30 минут
NO_DATA: Final[str] = 'Н/д'

bot_slash_commands: Final[dict[str, str]] = {
    SlashCommands.START: 'Старт',
    SlashCommands.HELP: 'Помощь',
    SlashCommands.SETTINGS: 'Настройки',
    SlashCommands.MENU: 'Меню',
    SlashCommands.LESSONS: 'Уроки',
    SlashCommands.CAFE: 'Столовая',
    SlashCommands.LAUNDRY: 'Прачечная',
    SlashCommands.ELECTIVES: 'Элективы',
    SlashCommands.EDUCATORS: 'Воспитатели',
    SlashCommands.CANCEL: 'Отмена ввода',
}
