from typing import Final

from bot.utils.enums import Meals, UserCallback


# Переводы всякого
CAFE_MENU_ENG_TO_RU: Final[dict[str, str]] = {
    Meals.BREAKFAST: "завтрак",
    Meals.LUNCH: "второй завтрак",
    Meals.DINNER: "обед",
    Meals.SNACK: "полдник",
    Meals.SUPPER: "ужин",
}
NOTIFIES_ENG_TO_RU: Final[dict[str, str]] = {
    "all": "всем",
    "grade_10": "десятикам",
    "grade_11": "одиннадцатым",
}
LAUNDRY_ENG_TO_RU: Final[dict[str, str]] = {
    UserCallback.WASHING: "время стирки",
    UserCallback.DRYING: "время сушки",
}

GRADES: Final[tuple[str, ...]] = ("10А", "10Б", "10В", "11А", "11Б", "11В")
BEAUTIFY_MEALS: Final[tuple[str, ...]] = (
    "🕗 Завтрак",
    "🕙 Второй завтрак",
    "🕐 Обед",
    "🕖 Полдник",
    "🕖 Ужин",
)

TODAY: Final[str] = "today"  # Использование сегодняшней даты
LAUNDRY_REPEAT: Final[int] = 30  # Повтор таймера прачечной через 30 минут
NOTIFIES_PER_BATCH: Final[int] = 20  # Сообщений за раз в рассылке
