from datetime import date

from cachetools.func import ttl_cache

from bot.database.db_funcs import Repository
from bot.utils.datehelp import format_date, date_today, weekday_by_date


@ttl_cache(ttl=60 * 60 * 24)  # Сутки
def format_menu(meals: tuple[str, ...]) -> str:
    """
    Формат дневного меню для сообщения в телегу.
    """

    return '\n\n'.join(
        f'*{meal_type}:*\n{meal or "Н/д"}'.strip()
        for meal_type, meal in zip(
            ('🕗Завтрак', '🕙Второй завтрак',
             '🕐Обед', '🕖Полдник', '🕖Ужин'),
            meals
        )
    ).strip()


# @ttl_cache(ttl=60 * 60)  # Час
async def get_formatted_menu_by_date(
        repo: Repository,
        menu_date: date = None
) -> str:
    """
    Возвращает меню (список строк) по дате.
    Н/д для каждого приёма пищи, если данных нет.

    :param repo: Доступ к базе данных.
    :param menu_date: Нужная дата.
    :return: Готовое сообщение для телеги.
    """

    if menu_date is None:
        menu_date = date_today()

    menu = await repo.get_menu_by_date(menu_date)

    meals = (
        menu.breakfast if menu and menu.breakfast else 'Н/д',
        menu.lunch if menu and menu.lunch else 'Н/д',
        menu.dinner if menu and menu.dinner else 'Н/д',
        menu.snack if menu and menu.snack else 'Н/д',
        menu.supper if menu and menu.supper else 'Н/д',
    )

    return f"🍺 *Меню на {format_date(menu_date)} " \
           f"({weekday_by_date(menu_date)})*:\n\n{format_menu(meals)}"