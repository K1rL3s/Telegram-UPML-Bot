from typing import TYPE_CHECKING

from sqlalchemy import select

from bot.database.models.educators_schedules import EducatorsSchedule
from bot.database.repository.base_repo import BaseRepository

if TYPE_CHECKING:
    import datetime as dt

    from sqlalchemy.ext.asyncio import AsyncSession


class EducatorsScheduleRepository(BaseRepository):
    """Класс для работы с расписаниями воспитателей в базе данных."""

    def __init__(self, session: "AsyncSession") -> None:
        self.session = session

    async def get(
        self,
        schedule_date: "dt.date",
    ) -> EducatorsSchedule | None:
        """
        Возвращает расписание воспитателей на день по дате.

        :param schedule_date: Дата запрашеваемого меню.
        :return: Модель EducatorsSchedule.
        """
        query = select(EducatorsSchedule).where(EducatorsSchedule.date == schedule_date)
        return await self.session.scalar(query)

    async def save_or_update_to_db(
        self,
        schedule_date: "dt.date",
        schedule_text: str,
        edit_by: int = 0,
    ) -> None:
        """
        Сохраняет или обновляет расписание воспитателей.

        :param schedule_date: Дата расписания.
        :param schedule_text: Текст расписания.
        :param edit_by: Кем редактируется.
        """
        if schedule := await self.get(schedule_date):
            schedule.schedule = schedule_text
            schedule.edit_by = edit_by
        else:
            schedule = EducatorsSchedule(
                date=schedule_date,
                schedule=schedule_text,
                edit_by=edit_by,
            )
            self.session.add(schedule)

        await self.session.commit()
