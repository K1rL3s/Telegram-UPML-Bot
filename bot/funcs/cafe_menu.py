from typing import TYPE_CHECKING

from cachetools.func import ttl_cache

from bot.utils.consts import CAFE_MENU_ENG_TO_RU, NO_DATA
from bot.utils.datehelp import date_today, format_date, weekday_by_date

if TYPE_CHECKING:
    import datetime as dt

    from bot.database.repository.repository import Repository


@ttl_cache(ttl=60 * 60 * 24)  # Сутки
def _format_menu(meals: tuple[str, ...]) -> str:
    """
    Формат дневного меню для сообщения в телегу.

    :param meals: Строки по порядку приёмов пищи.
    :return: Отформатированная строка с приёмами пищи.
    """
    return "\n\n".join(
        f"*{meal_type}:*\n{meal or NO_DATA}".strip()
        for meal_type, meal in zip(
            ("🕗Завтрак", "🕙Второй завтрак", "🕐Обед", "🕖Полдник", "🕖Ужин"),
            meals,
        )
    )


# @ttl_cache(ttl=60 * 60)  # Час
async def get_format_menu_by_date(
    repo: "Repository",
    menu_date: "dt.date" = None,
) -> str:
    """Возвращает меню по дате.

    Н/д для каждого приёма пищи, если данных нет.

    :param repo: Доступ к базе данных.
    :param menu_date: Нужная дата.
    :return: Готовое сообщение для телеги.
    """
    if menu_date is None:
        menu_date = date_today()

    menu = await repo.menu.get(menu_date)

    meals = tuple(
        getattr(menu, meal, NO_DATA) or NO_DATA for meal in CAFE_MENU_ENG_TO_RU
    )

    return (
        f"🍺 *Меню на {format_date(menu_date)} "
        f"({weekday_by_date(menu_date)})*:\n\n{_format_menu(meals).strip()}"
    )
