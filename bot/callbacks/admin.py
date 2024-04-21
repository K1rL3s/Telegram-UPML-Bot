from aiogram.filters.callback_data import CallbackData


class AdminEditMenu(CallbackData, prefix="admin_edit"):
    """Фабрика для изменения информации в каком-то из меню бота."""

    menu: str  # BotMenu


class AdminCheck(CallbackData, prefix="admin_check"):
    """Фабрика для просмотра одного админа."""

    user_id: int
    page: int = 0


class AdminEditRole(CallbackData, prefix="admin_role"):
    """Фабрика для редактирования ролей."""

    action: str | None = None
    role: str | None = None
    user_id: int | None = None


class EditMeal(CallbackData, prefix="edit_meal"):
    """Фабрика для выбора приёма пищи при изменении расписания еды."""

    meal: str  # Meal


class EditLessons(CallbackData, prefix="edit_lessons"):
    """Фабрика для выбора класса при изменении расписания."""

    grade: str  # 10, 11


class DoNotify(CallbackData, prefix="do_notify"):
    """Фабрика для рассылки уведомлений."""

    notify_type: str | None = None  # grade, class, all
    for_who: str | None = None  # 10, 11, 10А, 10Б, 10В, 11А, 11Б, 11В
