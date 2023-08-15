from datetime import date
from enum import Enum
from typing import Any, Type

import sqlalchemy as sa
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, MappedColumn, selectinload

from bot.database import (
    UserRelatedModel, ClassLessons, FullLessons,
    Laundry, Menu, Role, Settings, User,
)
from bot.database.models.educators_schedules import EducatorsSchedule
from bot.utils.consts import Roles, menu_eng_to_ru
from bot.utils.datehelp import datetime_now


class Repository:
    """
    Класс для вызова функций работы с базой данных.
    """

    def __init__(
            self,
            session: AsyncSession,
    ) -> None:
        self.session = session

    async def save_new_user(
            self,
            user_id: int,
            username: str,
    ) -> None:
        """
        Сохраняет пользователя в базе данных
        или обновляет его статус ``is_active``, никнейм,
        создаёт Settings и Laundry.

        :param user_id: Айди юзера.
        :param username: Имя пользователя.
        """
        user = await self.get_user(user_id)

        # Если юзер в бд и (он помечен как неактивный или изменился никнейм)
        if user and (not user.is_active or user.username != username):
            user.is_active = True
            user.username = username
        elif not user:
            user = User(user_id=user_id, username=username)
            self.session.add(user)
            logger.info(f'Новый пользователь {user}')

        await self.session.commit()

        await self.save_or_update_settings(user_id)
        await self.save_or_update_laundry(user_id)

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
            'breakfast': breakfast, 'lunch': lunch, 'dinner': dinner,
            'snack': snack, 'supper': supper
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
                'date': lessons_date,
                'grade': grade,
                'image': image,
            }
            if letter:
                data['letter'] = letter
            lessons = model(**data)
            self.session.add(lessons)

        await self.session.commit()

    async def save_or_update_laundry(
            self,
            user_id: int,
            **fields,
    ) -> None:
        """
        Сохраняет или обновляет уведомление о стирке/сушке.

        :param user_id: ТГ Айди.
        :param fields: Поле таблицы=значение.
        :return: Модель Laundry.
        """

        if laundry := await self.get_laundry(user_id):
            for k, v in fields.items():
                setattr(laundry, k, v)
        else:
            laundry = Laundry(user_id=user_id, **fields)
            self.session.add(laundry, )

        await self.session.commit()

    async def save_or_update_settings(
            self,
            user_id: int,
            **fields,
    ) -> None:
        """
        Создаёт или обнолвяет настройки пользователя.

        :param user_id: ТГ Айди.
        :param fields: Поле таблицы=значение.
        :return: модель Settings.
        """

        if settings := await self.get_settings(user_id):
            for k, v in fields.items():
                setattr(settings, k, v)
        else:
            settings = Settings(user_id=user_id, **fields)
            self.session.add(settings)

        await self.session.commit()

    async def save_or_update_educators_schedule(
            self,
            schedule_date: date,
            schedule_text: str,
            edit_by: int = 0,
    ) -> None:
        """
        Сохраняет или обновляет расписание воспитателей.

        :param schedule_date: Дата расписания.
        :param schedule_text: Текст расписания.
        :param edit_by: Кем редактируется.
        """

        schedule = await self.get_educators_schedule_by_date(schedule_date)

        if schedule:
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

    async def get_educators_schedule_by_date(
            self,
            schedule_date: date,
    ) -> EducatorsSchedule | None:
        """
        Возвращает расписание воспитателей на день по дате.

        :param schedule_date: Дата запрашеваемого меню.
        :return: Модель EducatorsSchedule.
        """
        query = sa.select(EducatorsSchedule).where(
            EducatorsSchedule.date == schedule_date
        )
        return await self.session.scalar(query)

    async def get_users_by_conditions(
            self,
            values: list[tuple[MappedColumn | Mapped, Any]],
            or_mode: bool = False,
    ) -> list[User]:
        """
        Возвращает список моделей User,
        у которых значение в настройках или пользователе совпадает с переданным

        :param values: Список из кортежей,
                       где первый элемент - колонка таблицы, второй - значение.
                       Пустой список - все юзеры.
        :param or_mode: Если True, то совпадение хотя бы по одному условию.
        :return: Список юзеров.
        """

        conditions = [(column == value) for column, value in values]
        conditions = sa.or_(*conditions) if or_mode else sa.and_(*conditions)
        query = sa.select(User).join(Settings).where(conditions)

        return list((await self.session.scalars(query)).all())

    async def get_role(
            self,
            role: Roles | str,
    ) -> Role | None:
        """
        Возвращает модель Role по названию роли.

        :param role: Название роли.
        :return: Модель Role.
        """

        if isinstance(role, Enum):
            role = role.value

        role_query = sa.select(Role).where(Role.role == role)
        return await self.session.scalar(role_query)

    async def get_users_with_role(
            self,
            role: Roles | str,
    ) -> list[User]:
        """
        Возвращает всех пользователей, у которых есть роль.

        :param role: Роль.
        :return: Список юзеров.
        """

        if isinstance(role, Enum):
            role = role.value

        subquery = sa.select(Role.id).where(Role.role == role)
        query = sa.select(User).where(
            User.roles.any(
                sa.cast(subquery.as_scalar(), sa.Boolean)
            )
        ).options(
            selectinload(User.roles)
        )

        return list((await self.session.scalars(query)).all())

    async def get_user_id_by_username(
            self,
            username: str,
    ) -> int | None:
        """
        Возвращает айди пользователя по его имени в базе.

        :param username: Имя юзера.
        :return: Айди юзера.
        """

        query = sa.select(User.user_id).where(User.username == username)
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
            FullLessons.date == lessons_date,
            FullLessons.grade == grade
        )
        return await self.session.scalar(query)

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
            ClassLessons.date == lessons_date,
            ClassLessons.class_ == class_
        )
        return await self.session.scalar(query)

    async def _get_model(
            self,
            model: Type[UserRelatedModel],
            user_id: int,
    ) -> UserRelatedModel | None:
        """
        Возвращает связанную с юзером модель по айди пользователя.

        :param model: Модель-наследник от UserRelatedModel.
        :param user_id: ТГ Айди юзера.
        :return: Модель model.
        """

        # noinspection PyTypeChecker
        query = sa.select(model).where(model.user_id == user_id)
        return await self.session.scalar(query)

    async def get_user(self, user_id: int) -> User | None:
        return await self._get_model(User, user_id)

    async def get_settings(self, user_id: int) -> Settings | None:
        return await self._get_model(Settings, user_id)

    async def get_laundry(self, user_id: int) -> Laundry | None:
        return await self._get_model(Laundry, user_id)

    async def get_expired_laundries(self) -> list[Laundry]:
        """
        Возвращает список моделей Laundry,
        у которых пришло время для уведомления.

        :return: Список из Laundry.
        """

        now = datetime_now()
        query = sa.select(Laundry).where(
            Laundry.is_active == True,  # noqa
            Laundry.end_time <= now
        )
        return list((await self.session.scalars(query)).all())

    async def update_user(
            self,
            user_id: int,
            **fields,
    ) -> None:
        """
        Обновление пользователя по айди.

        :param user_id: ТГ Айди юзера.
        :param fields: Поле таблицы=значение, ...
        """

        query = sa.update(User).where(
            User.user_id == user_id
        ).values(
            **fields
        )
        await self.session.execute(query)
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
        meals = {
            meal: getattr(menu, meal, None)
            for meal in menu_eng_to_ru.keys()
        }
        meals[meal] = new_menu

        await self.save_or_update_menu(
            menu_date=menu_date,
            edit_by=edit_by,
            **meals
        )

    async def is_has_any_role(
            self,
            user_id: int,
            roles: list[Roles | str] | tuple[Roles | str, ...],
    ) -> bool:
        """
        Имеет ли юзер хотя бы одну роль из переданных.

        :param user_id: ТГ Айди юзера.
        :param roles: Список ролей.
        :return: Тру или фэлс.
        """

        user = await self.get_user(user_id)
        if user is None:
            return False

        role_names = [
            role.value if isinstance(role, Enum) else role
            for role in roles
        ]
        return any(role.role in role_names for role in user.roles)

    async def remove_role_from_user(
            self,
            user_id: int,
            role: Roles | str,
    ) -> None:
        """
        Удаляет роль у юзера.

        :param user_id: ТГ Айди юзера.
        :param role: Его роль.
        """

        if isinstance(role, Roles):
            role = role.value

        user = await self.get_user(user_id)
        role = await self.get_role(role)

        try:
            user.roles.remove(role)
        except ValueError:
            pass

        await self.session.commit()

    async def add_role_to_user(
            self,
            user_id: int,
            role: Roles | str,
    ) -> None:
        """
        Добавляет роль юзеру.

        :param user_id: ТГ Айди юзера.
        :param role: Роль.
        """

        if isinstance(role, Roles):
            role = role.value

        user = await self.get_user(user_id)
        role = await self.get_role(role)

        user.roles.append(role)

        await self.session.commit()
