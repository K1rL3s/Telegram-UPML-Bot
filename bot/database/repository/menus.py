from datetime import date

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models.menus import Menu
from bot.database.repository.base_repo import BaseRepository
from bot.utils.consts import CAFE_MENU_ENG_TO_RU


class MenuRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_menu_by_date(
        self,
        menu_date: date,
    ) -> Menu | None:
        """
        Возвращает меню на день по дате.

        :param menu_date: Дата запрашеваемого меню.
        :return: Модель Menu.
        """

        query = sa.select(Menu).where(Menu.date == menu_date)
        return await self.session.scalar(query)

    async def save_or_update_menu(
        self,
        menu_date: date,
        breakfast: str | None = None,
        lunch: str | None = None,
        dinner: str | None = None,
        snack: str | None = None,
        supper: str | None = None,
        edit_by: int = 0,
    ) -> None:
        """
        Сохраняет или обновляет меню для определённой даты.

        :param menu_date: Дата меня.
        :param breakfast: Завтрак.
        :param lunch: Второй завтрак.
        :param dinner: Обед.
        :param snack: Полдник.
        :param supper: Ужин.
        :param edit_by: Кем редактируется, ТГ Айди, 0 - автоматически.
        """
        meals = {
            "breakfast": breakfast,
            "lunch": lunch,
            "dinner": dinner,
            "snack": snack,
            "supper": supper,
        }

        if menu := await self.get_menu_by_date(menu_date):
            for k, v in meals.items():
                # Если редактируется вручную или информации о еде нет:
                if edit_by or not getattr(menu, k, None):
                    setattr(menu, k, v)
            if edit_by:
                menu.edit_by = edit_by
        else:
            menu = Menu(
                **meals,
                edit_by=edit_by,
                date=menu_date,
            )
            self.session.add(menu)

        await self.session.commit()

    async def edit_menu_by_date(
        self,
        meal: str,
        new_menu: str,
        menu_date: date,
        edit_by: int,
    ) -> None:
        """
        Обновляет приём пищи по названию и дате вручную.

        :param meal: Название приёма пищи на английском.
        :param new_menu: Новая версия.
        :param menu_date: Дата.
        :param edit_by: ТГ Айди того, кто меняет.
        """

        menu = await self.get_menu_by_date(menu_date)
        meals = {meal: getattr(menu, meal, None) for meal in CAFE_MENU_ENG_TO_RU}
        meals[meal] = new_menu

        await self.save_or_update_menu(menu_date=menu_date, edit_by=edit_by, **meals)
