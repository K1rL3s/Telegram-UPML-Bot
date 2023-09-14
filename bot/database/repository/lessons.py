from typing import Optional, TYPE_CHECKING, Union

from sqlalchemy import delete, select

from bot.database.models.class_lessons import ClassLessons
from bot.database.models.full_lessons import FullLessons
from bot.database.repository.base_repo import BaseRepository

if TYPE_CHECKING:
    import datetime as dt

    from sqlalchemy.ext.asyncio import AsyncSession

    from bot.custom_types import LessonsAlbum


class LessonsRepository(BaseRepository):
    """Класс для работы с расписаниями уроков в базе данных."""

    def __init__(self, session: "AsyncSession") -> None:
        self._session = session

    async def get(
        self,
        date: "dt.date",
        class_or_grade: str,
    ) -> "Union[ClassLessons, FullLessons, None]":
        """
        Возвращает модель с айди изображением уроков на дату.

        :param date: Дата.
        :param class_or_grade: Класс в формате "10Б" или только паралелль (10 или 11).
        :return: Модель ClassLessons или FullLessons.
        """
        if class_or_grade.isdigit():
            return await self._get_full_lessons(date, class_or_grade)
        return await self._get_class_lessons(date, class_or_grade)

    async def save_or_update_to_db(
        self,
        image: str,
        date: "dt.date",
        grade: str,
        letter: str | None = None,
    ) -> None:
        """
        Сохраняет или обновляет уроки для паралелли.

        :param image: Айди изображения.
        :param date: Дата.
        :param grade: 10 или 11.
        :param letter: А, Б, В
        """
        model = ClassLessons if letter else FullLessons

        find_query = select(model).where(
            model.date == date,
            model.grade == grade,
        )

        if letter:
            find_query = find_query.where(model.letter == letter)

        if lessons := await self._session.scalar(find_query):
            lessons.image = image
        else:
            data = {
                "date": date,
                "grade": grade,
                "image": image,
            }
            if letter:
                data["letter"] = letter
            lessons = model(**data)
            self._session.add(lessons)

        await self._session.commit()

    async def save_prepared_to_db(
        self,
        lessons: "LessonsAlbum",
    ) -> None:
        """
        Сохранение готовых изображений расписаний уроков на дату для параллели.

        :param lessons: Полное изображение расписания уроков.
        """
        await self.save_or_update_to_db(
            lessons.full_photo_id,
            lessons.date,
            lessons.grade,
        )
        for class_photo_id, letter in zip(lessons.class_photo_ids, "АБВ"):
            await self.save_or_update_to_db(
                class_photo_id,
                lessons.date,
                lessons.grade,
                letter,
            )

    async def delete_class_lessons(
        self,
        date: "dt.date",
        grade: str,
    ) -> None:
        """
        Удаляет расписания для отдельных классов по дате и паралелли.

        :param date: Дата.
        :param grade: Параллель.
        """
        query = delete(ClassLessons).where(
            ClassLessons.date == date,
            ClassLessons.grade == grade,
        )
        await self._session.execute(query)
        await self._session.commit()

    async def _get_class_lessons(
        self,
        date: "dt.date",
        class_: str,
    ) -> "Optional[ClassLessons]":
        """
        Возвращает айди картинки расписания уроков для класса.

        :param date: Дата.
        :param class_: (10 или 11) + (А или Б или В) | (10А, 11Б, ...)
        :return: Айди картинки или None.
        """
        query = select(ClassLessons).where(
            ClassLessons.date == date,
            ClassLessons.class_ == class_,
        )
        return await self._session.scalar(query)

    async def _get_full_lessons(
        self,
        date: "dt.date",
        grade: str,
    ) -> "Optional[FullLessons]":
        """
        Возвращает айди картинки расписания уроков для параллели.

        :param date: Дата.
        :param grade: 10 или 11.
        :return: Айди картинки или None.
        """
        query = select(FullLessons).where(
            FullLessons.date == date,
            FullLessons.grade == grade,
        )
        return await self._session.scalar(query)
