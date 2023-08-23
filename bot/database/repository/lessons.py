from datetime import date

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models.class_lessons import ClassLessons
from bot.database.models.full_lessons import FullLessons
from bot.database.repository.base_repo import BaseRepository


class LessonsRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_class_lessons(
        self,
        lessons_date: date,
        class_: str,
    ) -> ClassLessons | None:
        """
        Возвращает айди картинки расписания уроков для класса.

        :param lessons_date: Дата.
        :param class_: (10 или 11) + (А или Б или В) | (10А, 11Б, ...)
        :return: Айди картинки или None.
        """

        query = sa.select(ClassLessons).where(
            ClassLessons.date == lessons_date, ClassLessons.class_ == class_
        )
        return await self.session.scalar(query)

    async def get_full_lessons(
        self,
        lessons_date: date,
        grade: str,
    ) -> FullLessons | None:
        """
        Возвращает айди картинки расписания уроков для параллели.

        :param lessons_date: Дата.
        :param grade: 10 или 11.
        :return: Айди картинки или None.
        """

        query = sa.select(FullLessons).where(
            FullLessons.date == lessons_date, FullLessons.grade == grade
        )
        return await self.session.scalar(query)

    async def save_or_update_lessons(
        self,
        image: str,
        lessons_date: date,
        grade: str,
        letter: str = None,
    ) -> None:
        """
        Сохраняет или обновляет уроки для паралелли.

        :param image: Айди изображения.
        :param lessons_date: Дата.
        :param grade: 10 или 11.
        :param letter: А, Б, В
        """

        model = ClassLessons if letter else FullLessons

        find_query = sa.select(model).where(
            model.date == lessons_date,
            model.grade == grade,
        )

        if letter:
            find_query = find_query.where(model.letter == letter)

        if lessons := await self.session.scalar(find_query):
            lessons.image = image
        else:
            data = {
                "date": lessons_date,
                "grade": grade,
                "image": image,
            }
            if letter:
                data["letter"] = letter
            lessons = model(**data)
            self.session.add(lessons)

        await self.session.commit()
