from enum import Enum


class SlashCommand(str, Enum):
    """Слэш команды бота."""

    START = "start"
    HELP = "help"
    SETTINGS = "settings"
    MENU = "menu"
    LESSONS = "lessons"
    CAFE = "cafe"
    LAUNDRY = "laundry"
    ELECTIVES = "electives"
    EDUCATORS = "educators"
    ENROLLEE = "enrollee"
    UNIVERS = "univers"
    OLYMPS = "olymps"
    CANCEL = "cancel"
    STOP = "stop"


class TextCommand(str, Enum):
    """Текстовые команды бота."""

    START = "Старт"
    HELP = "Помощь"
    SETTINGS = "⚙️Настройки"
    MENU = "Меню"
    LESSONS = "📓Уроки"
    CAFE = "🍴Меню"
    LAUNDRY = "💦Прачечная"
    ELECTIVES = "📖Элективы"
    EDUCATORS = "👩‍✈️Воспитатели"
    ENROLLEE = "📚 Поступающим"
    UNIVERS = "🏢 ВУЗы"
    OLYMPS = "🏆 Олимпиады"
    ADMIN_PANEL = "❗Админ панель"
    CANCEL = "Отмена"
    STOP = CANCEL


class NotifyType(str, Enum):
    """Типы уведомлений для пользователей."""

    ALL = "all"
    GRADE = "grade"
    CLASS = "class"
    GRADE_10 = "grade_10"
    GRADE_11 = "grade_11"


class Grade(str, Enum):
    """Учебные параллели."""

    GRADE_10 = "10"
    GRADE_11 = "11"


class BotMenu(str, Enum):
    """Callback'и для менюшек бота."""

    MAIN_MENU = "main_menu"
    SETTINGS = "settings"
    LAUNDRY = "laundry"
    EDUCATORS = "educators"
    ELECTIVES = "electives"
    CAFE_MENU = "cafe_menu"
    LESSONS = "lessons"
    ADMIN_PANEL = "admin_panel"
    NOTIFY = "notify"
    ENROLLEE = "enrollee"
    UNIVERS = "univers"
    OLYMPS = "olymps"


class PageMenu(str, Enum):
    """
    Callback'и для менюшек в менюшках.

    Чтобы не засорять BotMenu при использовании Paginator'а.
    """

    UNIVERS_LIST = "univers_list"
    OLYMPS_LIST = "olymps_list"


class Action(str, Enum):
    """Callback'и для действий пользователей."""

    OPEN = "open"
    CONFIRM = "confirm"
    START = "start"
    ADD = "add"
    SWITCH = "switch"
    EDIT = "edit"
    DELETE = "delete"
    CANCEL = "cancel"


class UserCallback(str, Enum):
    """Callback'и, которую используют все пользователей."""

    WASHING = "washing"
    DRYING = "drying"
    EMPTY = "empty"

    CHANGE_GRADE = "change_grade"
    LESSONS_NOTIFY = "lessons_notify"
    NEWS_NOTIFY = "news_notify"


class Meal(str, Enum):
    """Callback'и для названий приёмов пищи."""

    AUTO_ALL = "auto_all"
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"
    SUPPER = "supper"


class RoleEnum(str, Enum):
    """Роли (права доступа) пользователей."""

    SUPERADMIN = "superadmin"
    ADMIN = "admin"
    NOTIFY = "notify"
    LESSONS = "lessons"
    CAFE_MENU = "cafe_menu"
    EDUCATORS = "educators"
    UNIVERS = "univers"
    OLYMPS = "olymps"

    @staticmethod
    def all_roles() -> list[str]:
        """Все роли."""
        return [role.value if isinstance(role, Enum) else role for role in RoleEnum]

    @staticmethod
    def roles_which_can_be_edited() -> list[str]:
        """Роли, которые можно редактировать юзерам."""
        return [
            role.value if isinstance(role, Enum) else role
            for role in RoleEnum
            if role != RoleEnum.SUPERADMIN
        ]
