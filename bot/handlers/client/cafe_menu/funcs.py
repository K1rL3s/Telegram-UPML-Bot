from typing import TYPE_CHECKING

from cachetools.func import ttl_cache

from shared.utils.consts import BEAUTIFY_MEALS
from shared.utils.datehelp import format_date, weekday_by_date
from shared.utils.phrases import NO_DATA
from shared.utils.translate import CAFE_MENU_TRANSLATE

if TYPE_CHECKING:
    import datetime as dt

    from shared.database.repository import MenuRepository


# @ttl_cache(ttl=60 * 60)  # Час
async def get_format_menu_by_date(
    repo: "MenuRepository",
    date: "dt.date",
) -> str:
    """Возвращает меню по дате.

    Н/д для каждого приёма пищи, если данных нет.

    :param repo: Репозиторий расписаний столовой.
    :param date: Нужная дата.
    :return: Готовое сообщение для телеги.
    """
    menu = await repo.get(date)

    meals = tuple(
        getattr(menu, meal, NO_DATA) or NO_DATA for meal in CAFE_MENU_TRANSLATE
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
