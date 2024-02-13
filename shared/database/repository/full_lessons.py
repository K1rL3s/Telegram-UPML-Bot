import datetime as dt
from typing import Optional

from sqlalchemy import select

from shared.database.models.full_lessons import FullLessons
from shared.database.repository.base_repo import BaseRepository


class FullLessonsRepository(BaseRepository):
    """Класс для работы с полными расписаниями уроков в базе данных."""

    async def get(
        self,
        date: "dt.date",
        grade: str,
    ) -> "Optional[FullLessons]":
        """
        Возвращает уроки для параллели.

        :param date: Дата.
        :param grade: 10 или 11.
        :return: Айди картинки или None.
        """
        query = select(FullLessons).where(
            FullLessons.date == date,
            FullLessons.grade == grade,
        )
        return await self._session.scalar(query)

    async def save_or_update_to_db(
        self,
        file_id: str,
        date: "dt.date",
        grade: str,
    ) -> None:
        """
        Сохраняет или обновляет уроки для паралелли.

        :param file_id: Айди изображения.
        :param date: Дата.
        :param grade: 10 или 11.
        """
        if lessons := await self.get(date, grade):
            lessons.file_id = file_id
        else:
            lessons = FullLessons(
                date=date,
                grade=grade,
                file_id=file_id,
            )
            self._session.add(lessons)

        await self._session.flush()
