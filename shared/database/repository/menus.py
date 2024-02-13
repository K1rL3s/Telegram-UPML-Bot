import datetime as dt
from typing import Any

from sqlalchemy import select

from shared.database.models.menus import Menu
from shared.database.repository.base_repo import BaseRepository
from shared.utils.datehelp import date_today, get_this_week_monday
from shared.utils.translate import CAFE_MENU_TRANSLATE


class MenuRepository(BaseRepository):
    """Класс для работы с расписаниями столовой в базе данных."""

    async def get(
        self,
        date: "dt.date",
    ) -> Menu | None:
        """
        Возвращает меню столовой по дате.

        :param date: Дата.
        :return: Модель Menu.
        """
        query = select(Menu).where(Menu.date == date)
        return await self._session.scalar(query)

    async def save_or_update_to_db(
        self,
        date: "dt.date",
        **fields: Any,
    ) -> None:
        """
        Сохраняет или обновляет меню для определённой даты.

        :param date: Дата меня.
        :param fields: Ключ - колонка, значение - новое значение.
        """
        edit_by = fields.pop("edit_by", None)

        if menu := await self.get(date):
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
                date=date,
            )
            self._session.add(menu)

        await self._session.flush()

    async def update(
        self,
        meal: str,
        new_menu: str,
        date: "dt.date",
        edit_by: int,
    ) -> None:
        """
        Обновляет приём пищи по названию и дате вручную.

        :param meal: Название приёма пищи на английском.
        :param new_menu: Новая версия.
        :param date: Дата.
        :param edit_by: ТГ Айди того, кто меняет.
        """
        menu = await self.get(date)
        meals = {meal: getattr(menu, meal, None) for meal in CAFE_MENU_TRANSLATE}
        meals[meal] = new_menu

        await self.save_or_update_to_db(date=date, edit_by=edit_by, **meals)

    async def is_filled_on_today(self) -> bool:
        """
        Заполнено ли расписание еды на сегодня (неделю).

        :return: Бул.
        """
        monday_menu = await self.get(get_this_week_monday())
        today_menu = await self.get(date_today())
        return bool(monday_menu and today_menu)
