from typing import Final

from shared.utils.enums import Meals, Roles, UserCallback

CAFE_MENU_TRANSLATE: Final[dict[str, str]] = {
    Meals.BREAKFAST: "завтрак",
    Meals.LUNCH: "второй завтрак",
    Meals.DINNER: "обед",
    Meals.SNACK: "полдник",
    Meals.SUPPER: "ужин",
}
NOTIFIES_TYPES_TRANSLATE: Final[dict[str, str]] = {
    "all": "всем",
    "grade_10": "десятикам",
    "grade_11": "одиннадцатым",
}
LAUNDRY_TIMERS_TRANSLATE: Final[dict[str, str]] = {
    UserCallback.WASHING: "время стирки",
    UserCallback.DRYING: "время сушки",
}
ROLES_TRANSLATE: Final[dict[str, str]] = {
    Roles.SUPERADMIN: "супер-админ",
    Roles.ADMIN: "админ",
    Roles.NOTIFY: "уведомления",
    Roles.LESSONS: "уроки",
    Roles.CAFE_MENU: "столовая",
    Roles.EDUCATORS: "воспитатели",
}
