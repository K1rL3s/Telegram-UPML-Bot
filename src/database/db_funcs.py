from datetime import date
from enum import Enum
from typing import Any, Type

import sqlalchemy as sa
from loguru import logger
from sqlalchemy.orm import selectinload

from src.database.__all_models import (
    BaseModel, ClassLessons, FullLessons,
    Laundry, Menu, Role, Settings, User,
)
from src.database.db_session import get_session
from src.utils.consts import Roles, menu_eng_to_ru
from src.utils.datehelp import datetime_now


async def save_new_user(user_id: int, username: str) -> None:
    """
    Сохраняет пользователя в базе данных
    или обновляет его статус ``is_active``, никнейм,
    создаёт Settings и Laundry.

    :param user_id: Айди юзера.
    :param username: Имя пользователя.
    """

    async with get_session() as session:
        user_query = sa.select(User).where(User.user_id == user_id)
        user: User = await session.scalar(user_query)

        if user and (not user.is_active or user.username != username):
            user.is_active = True
            user.username = username
        elif not user:
            user = User(user_id=user_id, username=username)
            session.add(user)
            logger.info(f'Новый пользователь {user}')

        await session.commit()

    await save_or_update_settings(user_id)
    await save_or_update_laundry(user_id)


async def save_or_update_menu_in_db(
        menu_date: date,
        breakfast: str | None = None,
        lunch: str | None = None,
        dinner: str | None = None,
        snack: str | None = None,
        supper: str | None = None,
        edit_by: int = 0
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

    async with get_session() as session:
        user_db_id = (await get_user(edit_by)).id if edit_by != 0 else None
        find_query = sa.select(Menu).where(Menu.date == menu_date)
        meals = {
            'breakfast': breakfast, 'lunch': lunch, 'dinner': dinner,
            'snack': snack, 'supper': supper
        }

        if menu := await session.scalar(find_query):
            for k, v in meals.items():
                if edit_by or not getattr(menu, k, None):
                    setattr(menu, k, v)
            if user_db_id:
                menu.edit_by = user_db_id
        else:
            menu = Menu(
                **meals,
                edit_by=user_db_id,
                date=menu_date,
            )
            session.add(menu)

        await session.commit()


async def save_or_update_lessons(
        image: str,
        lessons_date: date,
        grade: str,
        letter: str = None
) -> None:
    """
    Сохраняет или обновляет уроки для паралелли.

    :param image: Айди изображения.
    :param lessons_date: Дата.
    :param grade: 10 или 11.
    :param letter: А, Б, В
    """

    model = ClassLessons if letter else FullLessons

    async with get_session() as session:
        find_query = sa.select(model).where(
            model.date == lessons_date,
            model.grade == grade,
        )

        if letter:
            find_query = find_query.where(model.letter == letter)

        if lessons := await session.scalar(find_query):
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
            session.add(lessons)

        await session.commit()


async def save_or_update_laundry(
        user_id: int,
        **kwargs
) -> None:
    """
    Сохраняет или обновляет уведомление о стирке/сушке.

    :param user_id: ТГ Айди.
    :param kwargs: Поле таблицы=значение.
    :return: Модель Laundry.
    """

    async with get_session() as session:
        db_user_id_query = sa.select(User.id).where(User.user_id == user_id)
        db_user_id = await session.scalar(db_user_id_query)

        # noinspection PyTypeChecker
        query = sa.select(Laundry).where(Laundry.user_id == db_user_id)

        if laundry := await session.scalar(query):
            for k, v in kwargs.items():
                setattr(laundry, k, v)
        else:
            laundry = Laundry(user_id=db_user_id)
            session.add(laundry)

        await session.commit()


async def save_or_update_settings(
        user_id: int,
        **kwargs
) -> None:
    """
    Создаёт или обнолвяет настройки пользователя.

    :param user_id: ТГ Айди.
    :param kwargs: Поле таблицы=значение.
    :return: модель Settings.
    """
    async with get_session() as session:
        db_user_id_query = sa.select(User.id).where(User.user_id == user_id)
        db_user_id = await session.scalar(db_user_id_query)

        # noinspection PyTypeChecker
        query = sa.select(Settings).where(Settings.user_id == db_user_id)

        if settings := await session.scalar(query):
            for k, v in kwargs.items():
                setattr(settings, k, v)
        else:
            settings = Settings(
                user_id=db_user_id,
                **kwargs
            )
            session.add(settings)

        await session.commit()


async def get_menu_by_date(menu_date: date) -> Menu | None:
    """
    Возвращает меню на день по дате.

    :param menu_date: Дата запрашеваемого меню.
    :return: Модель Menu.
    """

    async with get_session() as session:
        query = sa.select(Menu).where(Menu.date == menu_date)
        return await session.scalar(query)


async def get_users_by_conditions(
        values: list[tuple[str, Any]],
        or_mode: bool = False
) -> list[User]:
    """
    Возвращает список моделей User,
    у которых значение в настройках или пользователе совпадает с переданным.

    :param values: Список из кортежей,
                   где первый элемент - колонка, второй - значение.
                   Пустой список - все юзеры.
    :param or_mode: Если True, то совпадение хотя бы по одному условию.
    :return: Список юзеров.
    """

    async with get_session() as session:
        conditions = []
        for attr, value in values:
            if hasattr(User, attr):
                conditions.append(getattr(User, attr) == value)
            else:
                conditions.append(getattr(Settings, attr) == value)

        if or_mode:
            query = sa.select(User).join(Settings).where(
                sa.or_(*conditions)
            )
        else:
            query = sa.select(User).join(Settings).where(
                sa.and_(*conditions)
            )
        return list((await session.scalars(query)).all())


# ???
async def get_role(role: Roles | str) -> Role | None:
    """
    Возвращает модель Role по названию роли.

    :param role: Название роли.
    :return: Модель Role.
    """

    if isinstance(role, Enum):
        role = role.value

    async with get_session() as session:
        role_query = sa.select(Role).where(Role.role == role)
        return await session.scalar(role_query)


async def get_users_with_role(role: Roles | str) -> list[User]:
    """
    Возвращает всех пользователей, у которых есть роль.

    :param role: Роль.
    :return: Список юзеров.
    """

    if isinstance(role, Enum):
        role = role.value

    async with get_session() as session:
        subquery = sa.select(Role.id).where(Role.role == role)
        query = sa.select(User).where(
            User.roles.any(
                sa.cast(subquery.as_scalar(), sa.Boolean)
            )
        ).options(selectinload(User.roles))

        return list((await session.scalars(query)).all())


async def get_user_id_by_username(username: str) -> int | None:
    """
    Возвращает айди пользователя по его имени в базе.

    :param username: Имя юзера.
    :return: Айди юзера.
    """

    async with get_session() as session:
        query = sa.select(User.user_id).where(User.username == username)
        return await session.scalar(query)


async def get_full_lessons(lessons_date: date, grade: str) -> str | None:
    """
    Возвращает айди картинки расписания уроков для параллели.

    :param lessons_date: Дата.
    :param grade: 10 или 11.
    :return: Айди картинки или None.
    """

    async with get_session() as session:
        query = sa.select(FullLessons).where(
            FullLessons.date == lessons_date,
            FullLessons.grade == grade
        )
        lessons: FullLessons = await session.scalar(query)
        return lessons.image if lessons else None


async def get_class_lessons(
        lessons_date: date,
        class_: str
) -> str | None:
    """
    Возвращает айди картинки расписания уроков для класса.

    :param lessons_date: Дата.
    :param class_: (10 или 11) + (А, Б, В) .
    :return: Айди картинки или None.
    """

    async with get_session() as session:
        query = sa.select(ClassLessons).where(
            ClassLessons.date == lessons_date,
            ClassLessons.class_ == class_
        )
        lessons: ClassLessons = await session.scalar(query)
        return lessons.image if lessons else None


async def _get_model(
        model: Type[BaseModel],
        user_id: int,
        do_subquery: bool = False
) -> BaseModel | None:
    """
    Возвращает модель Model по айди пользователя.

    :param model: Модель из папки models.
    :param user_id: ТГ Айди юзера.
    :param do_subquery: Делать ли подзапрос
                        (для моделей, связанных с users.id).
    :return: Модель model.
    """

    async with get_session() as session:
        query = sa.select(model)

        if do_subquery:
            query = query.where(
                model.user_id == (
                    sa.select(User.id).where(
                        User.user_id == user_id
                    )
                ).scalar_subquery()
            )
        else:
            query = query.where(model.user_id == user_id)

        return await session.scalar(query)


async def get_user(user_id: int) -> User | None:
    return await _get_model(User, user_id)


async def get_settings(user_id: int) -> Settings | None:
    return await _get_model(Settings, user_id, do_subquery=True)


async def get_laundry(user_id: int) -> Laundry | None:
    return await _get_model(Laundry, user_id, do_subquery=True)


async def get_expired_laundries() -> list[Laundry]:
    """
    Возвращает список моделей Laundry, у которых пришло время для уведомления.

    :return: Список из Laundry.
    """

    async with get_session() as session:
        now = datetime_now()
        query = sa.select(Laundry).where(
            Laundry.is_active == True,
            Laundry.end_time <= now
        )
        return list((await session.scalars(query)).all())


async def update_user(user_id: int, **params) -> None:
    """
    Обновление пользователя по айди.

    :param user_id: ТГ Айди юзера.
    :param params: Поле таблицы=значение, ...
    """

    async with get_session() as session:
        query = sa.update(User).where(
            User.user_id == user_id
        ).values(
            **params
        )
        await session.execute(query)
        await session.commit()


async def edit_meal_by_date(
        meal: str,
        new_menu: str,
        menu_date: date,
        edit_by: int
) -> None:
    """
    Обновляет приём пищи по названию и дате вручную.

    :param meal: Название приёма пищи на английском.
    :param new_menu: Новая версия.
    :param menu_date: Дата.
    :param edit_by: ТГ Айди того, кто меняет.
    """
    menu = await get_menu_by_date(menu_date)

    meals = {
        meal: getattr(menu, meal, None)
        for meal in menu_eng_to_ru.keys()
    }
    meals[meal] = new_menu

    await save_or_update_menu_in_db(
        menu_date=menu_date,
        edit_by=edit_by,
        **meals
    )


async def is_has_any_role(user_id: int, roles: list[Roles | str]) -> bool:
    """
    Имеет ли юзер хотя бы одну роль из переданных.

    :param user_id: ТГ Айди юзера.
    :param roles: Список ролей.
    :return: Тру или фэлс.
    """

    async with get_session() as session:
        user_query = sa.select(User).where(User.user_id == user_id)
        user: User = await session.scalar(user_query)
        if user is None:
            return False

        role_names = [
            role.value if isinstance(role, Enum) else role
            for role in roles
        ]
        return any(role.role in role_names for role in user.roles)


async def remove_role_from_user(user_id: int, role: Roles | str) -> None:
    """
    Удаляет роль у юзера.

    :param user_id: ТГ Айди юзера.
    :param role: Его роль.
    """

    if isinstance(role, Roles):
        role = role.value

    async with get_session() as session:
        user_query = sa.select(User).where(User.user_id == user_id)
        role_query = sa.select(Role).where(Role.role == role)
        user = await session.scalar(user_query)
        role = await session.scalar(role_query)

        try:
            user.roles.remove(role)
        except ValueError:
            pass

        await session.commit()


async def add_role_to_user(user_id: int, role: Roles | str) -> None:
    """
    Добавляет роль юзеру.

    :param user_id: ТГ Айди юзера.
    :param role: Роль.
    """

    if isinstance(role, Roles):
        role = role.value

    async with get_session() as session:
        user_query = sa.select(User).where(User.user_id == user_id)
        role_query = sa.select(Role).where(Role.role == role)
        user = await session.scalar(user_query)
        role = await session.scalar(role_query)
        user.roles.append(role)

        await session.commit()
