from enum import Enum


class SlashCommands(str, Enum):
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
    CANCEL = "cancel"
    STOP = "stop"


class TextCommands(str, Enum):
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
    ADMIN_PANEL = "❗Админ панель"
    CANCEL = "Отмена"
    STOP = CANCEL


class NotifyTypes(str, Enum):
    """Типы уведомлений для пользователей."""

    ALL = "all"
    GRADE = "grade"
    CLASS = "class"
    GRADE_10 = "grade_10"
    GRADE_11 = "grade_11"


class Grades(str, Enum):
    """Учебные параллели."""

    GRADE_10 = "10"
    GRADE_11 = "11"


class Menus(str, Enum):
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


class Actions(str, Enum):
    """Callback'и для действий пользователей."""

    CONFIRM = "confirm"
    START = "start"
    ADD = "add"
    CHECK = "check"
    SWITCH = "switch"
    EDIT = "edit"
    REMOVE = "remove"
    CANCEL = "cancel"


class UserCallback(str, Enum):
    """Callback'и, которую используют все пользователей."""

    WASHING = "washing"
    DRYING = "drying"
    EMPTY = "empty"

    CHANGE_GRADE = "change_grade"
    LESSONS_NOTIFY = "lessons_notify"
    NEWS_NOTIFY = "news_notify"


class Meals(str, Enum):
    """Callback'и для названий приёмов пищи."""

    AUTO_ALL = "auto_all"
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"
    SUPPER = "supper"


class Roles(str, Enum):
    """Роли (права доступа) пользователей."""

    SUPERADMIN = "superadmin"
    ADMIN = "admin"
    NOTIFY = "notify"
    LESSONS = "lessons"
    CAFE_MENU = "cafe_menu"
    EDUCATORS = "educators"

    @staticmethod
    def all_roles() -> list[str]:
        """Все роли."""
        return [role.value if isinstance(role, Enum) else role for role in Roles]

    @staticmethod
    def roles_which_can_be_edited() -> list[str]:
        """Роли, которые можно редактировать юзерам."""
        return [
            role.value if isinstance(role, Enum) else role
            for role in Roles
            if role != Roles.SUPERADMIN
        ]
