import datetime as dt

from sqlalchemy import select

from shared.database.models.educators_schedules import EducatorsSchedule
from shared.database.repository.base_repo import BaseRepository


class EducatorsScheduleRepository(BaseRepository):
    """Класс для работы с расписаниями воспитателей в базе данных."""

    async def get(
        self,
        date: "dt.date",
    ) -> EducatorsSchedule | None:
        """
        Возвращает расписание воспитателей по дате.

        :param date: Дата запрашеваемого меню.
        :return: Модель EducatorsSchedule.
        """
        query = select(EducatorsSchedule).where(EducatorsSchedule.date == date)
        return await self._session.scalar(query)

    async def save_or_update_to_db(
        self,
        date: "dt.date",
        schedule_text: str,
        edit_by: int | None = None,
    ) -> None:
        """
        Сохраняет или обновляет расписание воспитателей.

        :param date: Дата расписания.
        :param schedule_text: Текст расписания.
        :param edit_by: Кем редактируется.
        """
        if schedule := await self.get(date):
            schedule.schedule = schedule_text
            schedule.edit_by = edit_by
        else:
            schedule = EducatorsSchedule(
                date=date,
                schedule=schedule_text,
                edit_by=edit_by,
            )
            self._session.add(schedule)

        await self._session.flush()
