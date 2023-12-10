from typing import Final

GRADES: Final[tuple[str, ...]] = ("10А", "10Б", "10В", "11А", "11Б", "11В")
BEAUTIFY_MEALS: Final[tuple[str, ...]] = (
    "🕗 Завтрак",
    "🕙 Второй завтрак",
    "🕐 Обед",
    "🕖 Полдник",
    "🕖 Ужин",
)

TODAY: Final[str] = "today"  # Использование сегодняшней даты
REPEAT_LAUNDRY_TIMER: Final[int] = 30  # Повтор таймера прачечной через 30 минут
NOTIFIES_PER_BATCH: Final[int] = 20  # Сообщений за раз в рассылке
