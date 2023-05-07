from datetime import date

import sqlalchemy as sa

from src.database.menu import Menu
from src.database.db_session import create_session


def save_menu_in_db(
        menu_date: date,
        breakfast: str,
        lunch: str,
        dinner: str,
        snack: str,
        supper: str,
) -> None:
    """
    Сохраняет меню для определённой даты.

    :param menu_date: Дата меня.
    :param breakfast: Завтрак.
    :param lunch: Второй завтрак.
    :param dinner: Обед.
    :param snack: Полдник.
    :param supper: Ужин.
    """

    with create_session(do_commit=True) as session:
        find_query = sa.Select(Menu).where(Menu.date == menu_date)
        if session.scalar(find_query):
            delete_query = sa.Delete(Menu).where(Menu.date == menu_date)
            session.execute(delete_query)

        menu = Menu(
            date=menu_date,
            breakfast=breakfast,
            lunch=lunch,
            dinner=dinner,
            snack=snack,
            supper=supper
        )
        session.add(menu)


def get_menu_by_date(
        menu_date: date
) -> Menu:
    """
    Возвращает меню на день по дате.

    :param menu_date: Дата запрашеваемого меню.
    :return: Модель Меню.
    """

    with create_session() as session:
        query = sa.Select(Menu).where(Menu.date == menu_date)
        return session.scalar(query)
