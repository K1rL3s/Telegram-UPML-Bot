from typing import Any, TYPE_CHECKING

from sqlalchemy import select

from bot.database.models.menus import Menu
from bot.database.repository.base_repo import BaseRepository
from bot.utils.consts import CAFE_MENU_ENG_TO_RU

if TYPE_CHECKING:
    import datetime as dt

    from sqlalchemy.ext.asyncio import AsyncSession


class MenuRepository(BaseRepository):
    """Класс для работы с расписаниями столовой в базе данных."""

    def __init__(self, session: "AsyncSession") -> None:
        self.session = session

    async def get(
        self,
        menu_date: "dt.date",
    ) -> Menu | None:
        """
        Возвращает меню на день по дате.

        :param menu_date: Дата запрашеваемого меню.
        :return: Модель Menu.
        """
        query = select(Menu).where(Menu.date == menu_date)
        return await self.session.scalar(query)

    async def save_or_update_to_db(
        self,
        menu_date: "dt.date",
        edit_by: int | None = None,
        **fields: Any,
    ) -> None:
        """
        Сохраняет или обновляет меню для определённой даты.

        :param menu_date: Дата меня.
        :param edit_by: Кем редактируется, ТГ Айди, 0 - автоматически.
        :param fields: Ключ - колонка, значение - новое значение.
        """
        if menu := await self.get(menu_date):
            for k, v in fields.items():
                # Если редактируется вручную или информации о еде нет:
                if edit_by or not getattr(menu, k, None):
                    setattr(menu, k, v)
            if edit_by:
                menu.edit_by = edit_by
        else:
            menu = Menu(
                **fields,
                edit_by=edit_by,
                date=menu_date,
            )
            self.session.add(menu)

        await self.session.commit()

    async def update(
        self,
        meal: str,
        new_menu: str,
        menu_date: "dt.date",
        edit_by: int,
    ) -> None:
        """
        Обновляет приём пищи по названию и дате вручную.

        :param meal: Название приёма пищи на английском.
        :param new_menu: Новая версия.
        :param menu_date: Дата.
        :param edit_by: ТГ Айди того, кто меняет.
        """
        menu = await self.get(menu_date)
        meals = {meal: getattr(menu, meal, None) for meal in CAFE_MENU_ENG_TO_RU}
        meals[meal] = new_menu

        await self.save_or_update_to_db(menu_date=menu_date, edit_by=edit_by, **meals)
