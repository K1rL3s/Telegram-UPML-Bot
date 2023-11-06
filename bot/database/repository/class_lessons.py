from typing import TYPE_CHECKING, Optional

from sqlalchemy import delete, select

from bot.database.models.class_lessons import ClassLessons
from bot.database.repository.base_repo import BaseRepository

if TYPE_CHECKING:
    import datetime as dt

    from sqlalchemy.ext.asyncio import AsyncSession


class ClassLessonsRepository(BaseRepository):
    """Класс для работы с расписаниями уроков в базе данных."""

    def __init__(self, session: "AsyncSession") -> None:
        self._session = session

    async def delete(
        self,
        date: "dt.date",
        grade: str,
    ) -> None:
        """
        Удаляет отдельные расписания для классов по дате и паралелли.

        :param date: Дата.
        :param grade: Параллель.
        """
        query = delete(ClassLessons).where(
            ClassLessons.date == date,
            ClassLessons.grade == grade,
        )
        await self._session.execute(query)
        await self._session.flush()

    async def get(
        self,
        date: "dt.date",
        class_: str,
    ) -> "Optional[ClassLessons]":
        """
        Возвращает ClassLessons для класса.

        :param date: Дата.
        :param class_: (10 или 11) + (А или Б или В) = (10А, 11Б, ...)
        :return: Модель ClassLessons.
        """
        query = select(ClassLessons).where(
            ClassLessons.date == date,
            ClassLessons.class_ == class_,
        )
        return await self._session.scalar(query)

    async def save_or_update_to_db(
        self,
        file_id: str,
        date: "dt.date",
        grade: str,
        letter: str,
    ) -> None:
        """
        Сохраняет или обновляет уроки для класса.

        :param file_id: Айди изображения.
        :param date: Дата.
        :param grade: 10 или 11.
        :param letter: А, Б, В
        """
        if lessons := await self.get(date, f"{grade}{letter}"):
            lessons.file_id = file_id
        else:
            lessons = ClassLessons(
                date=date,
                file_id=file_id,
                grade=grade,
                letter=letter,
            )
            self._session.add(lessons)

        await self._session.flush()
