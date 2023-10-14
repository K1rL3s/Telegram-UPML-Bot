from aiogram.filters.callback_data import CallbackData


class AdminEditData(CallbackData, prefix="admin_edit"):
    """Фабрика для изменения информации в каком-то из меню бота."""

    menu: str  # Menus


class AdminListData(CallbackData, prefix="admin_list"):
    """Фабрика для просмотра списка админов."""

    page: int = 0


class AdminManageData(CallbackData, prefix="admin_manage"):
    """Фабрика для просмотра, добавления и удаления админов."""

    action: str
    user_id: int | None = None
    is_sure: bool = False
    page: int = 0


class EditMealData(CallbackData, prefix="edit_cafe_menu"):
    """Фабрика для выбора приёма пищи при изменении расписания еды."""

    meal: str  # Meals


class EditLessonsData(CallbackData, prefix="edit_lessons"):
    """Фабрика для выбора класса при изменении расписания."""

    grade: str  # 10, 11


class DoNotifyData(CallbackData, prefix="notify"):
    """Фабрика для рассылки уведомления."""

    notify_type: str | None = None  # grade, class, all
    for_who: str | None = None  # 10, 11, 10А, 10Б, 10В, 11А, 11Б, 11В
