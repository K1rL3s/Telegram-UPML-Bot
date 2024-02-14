from typing import Final

from shared.utils.enums import Meal, RoleEnum, UserCallback

CAFE_MENU_TRANSLATE: Final[dict[str, str]] = {
    Meal.BREAKFAST: "завтрак",
    Meal.LUNCH: "второй завтрак",
    Meal.DINNER: "обед",
    Meal.SNACK: "полдник",
    Meal.SUPPER: "ужин",
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
    RoleEnum.SUPERADMIN: "супер-админ",
    RoleEnum.ADMIN: "админ",
    RoleEnum.NOTIFY: "уведомления",
    RoleEnum.LESSONS: "уроки",
    RoleEnum.CAFE_MENU: "столовая",
    RoleEnum.EDUCATORS: "воспитатели",
    RoleEnum.UNIVERS: "университеты",
    RoleEnum.OLYMPS: "олимпиады",
}
