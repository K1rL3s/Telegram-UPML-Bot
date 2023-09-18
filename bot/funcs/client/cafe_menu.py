from typing import TYPE_CHECKING

from cachetools.func import ttl_cache

from bot.utils.consts import BEAUTIFY_MEALS, CAFE_MENU_ENG_TO_RU
from bot.utils.phrases import NO_DATA
from bot.utils.datehelp import date_today, format_date, weekday_by_date

if TYPE_CHECKING:
    import datetime as dt

    from bot.database.repository import MenuRepository


# @ttl_cache(ttl=60 * 60)  # Час
async def get_format_menu_by_date(
    repo: "MenuRepository",
    date: "dt.date" = None,
) -> str:
    """Возвращает меню по дате.

    Н/д для каждого приёма пищи, если данных нет.

    :param repo: Репозиторий расписаний столовой.
    :param date: Нужная дата.
    :return: Готовое сообщение для телеги.
    """
    if date is None:
        date = date_today()

    menu = await repo.get(date)

    meals = tuple(
        getattr(menu, meal, NO_DATA) or NO_DATA for meal in CAFE_MENU_ENG_TO_RU
    )

    return (
        f"🍺 <b>Меню на {format_date(date)} ({weekday_by_date(date)})</b>:\n\n"
        f"{_format_menu(meals).strip()}"
    )


@ttl_cache(ttl=60 * 60 * 24)  # Сутки
def _format_menu(meals: tuple[str, ...]) -> str:
    """
    Формат дневного меню для сообщения в телегу.

    :param meals: Строки по порядку приёмов пищи.
    :return: Отформатированная строка с приёмами пищи.
    """
    return "\n\n".join(
        f"<b>{meal_type}:</b>\n{meal or NO_DATA}".strip()
        for meal_type, meal in zip(
            BEAUTIFY_MEALS,
            meals,
        )
    )
