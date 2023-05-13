from datetime import date
from enum import Enum
from typing import Any

import sqlalchemy as sa

from src.database.models.class_lessons import ClassLessons
from src.database.models.full_lessons import FullLessons
from src.database.models.menus import Menu
from src.database.models.roles import Role
from src.database.models.users import User
from src.database.db_session import create_session
from src.utils.consts import Roles, menu_eng_to_ru


def save_user_or_update_status(user_id: int, username: str) -> None:
    """
    Сохраняет пользователя в базе данных
    или обновляет его статус ``is_active`` и никнейм.

    :param user_id: Айди юзера.
    :param username: Имя пользователя.
    """

    with create_session(do_commit=True) as session:
        query = sa.Select(User).where(User.user_id == user_id)
        user: User = session.scalar(query)

        if user and (not user.is_active or user.username != username):
            user.is_active = True
            user.username = username
        elif not user:
            user = User(user_id=user_id, username=username)
            session.add(user)


def save_or_update_menu_in_db(
        menu_date: date,
        breakfast: str | None,
        lunch: str | None,
        dinner: str | None,
        snack: str | None,
        supper: str | None,
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
    :param edit_by: Кем редактируется, айди в бд, 0 - автоматически.
    """

    with create_session(do_commit=True) as session:
        find_query = sa.Select(Menu).where(Menu.date == menu_date)
        if menu := session.scalar(find_query):
            # Если меню кем-то редактировалось
            # и сейчас обновляется автоматически
            if menu.edit_by and not edit_by:
                return
            menu.breakfast = breakfast
            menu.lunch = lunch
            menu.dinner = dinner
            menu.snack = snack
            menu.supper = supper
            menu.edit_by = edit_by
        else:
            menu = Menu(
                date=menu_date,
                breakfast=breakfast,
                lunch=lunch,
                dinner=dinner,
                snack=snack,
                supper=supper,
                edit_by=edit_by
            )
            session.add(menu)


def save_or_update_lessons(
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

    with create_session(do_commit=True) as session:
        find_query = sa.Select(model).where(
            model.date == lessons_date,
            model.grade == grade,
        )

        if letter:
            find_query = find_query.where(model.letter == letter)

        if lessons := session.scalar(find_query):
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


def get_menu_by_date(menu_date: date) -> Menu | None:
    """
    Возвращает меню на день по дате.

    :param menu_date: Дата запрашеваемого меню.
    :return: Модель Menu.
    """

    with create_session() as session:
        query = sa.Select(Menu).where(Menu.date == menu_date)
        return session.scalar(query)


def get_user(user_id: int) -> User | None:
    """
    Возвращает модель User по айди пользователя.

    :param user_id: Айди юзера.
    :return: Модель User.
    """

    with create_session() as session:
        query = sa.Select(User).where(User.user_id == user_id)
        return session.scalar(query)


def get_users_by_conditions(
        values: list[tuple[str, Any]],
        or_mode: bool = False
) -> list[User]:
    """
    Возвращает список моделей User,
    у которых значение в колонке совпадает с переданным.

    :param values: Список из кортежей,
                   где первый элемент - колонка, второй - значение.
                   Пустой список - все юзеры.
    :param or_mode: Если True, то совпадение хотя бы по одному условию.
    :return: Список юзеров.
    """

    with create_session() as session:
        conditions = []
        for attr, value in values:
            conditions.append(getattr(User, attr) == value)

        if or_mode:
            find_query = sa.select(User).where(sa.or_(*conditions))
        else:
            find_query = sa.select(User).where(sa.and_(*conditions))

        return list(session.scalars(find_query).all())


def get_role(role: Roles | str) -> Role | None:
    """
    Возвращает модель Role по названию роли.

    :param role: Название роли.
    :return: Модель Role.
    """

    if isinstance(role, Enum):
        role = role.value

    with create_session() as session:
        role_query = sa.select(Role).where(Role.role == role)
        return session.scalar(role_query)


def get_users_with_role(role: Roles | str) -> list[User]:
    """
    Возвращает всех пользователей, у которых есть роль.

    :param role: Роль.
    :return: Список юзеров.
    """

    if isinstance(role, Enum):
        role = role.value

    with create_session() as session:
        query = sa.select(User).where(
            User.roles.any(
                sa.select(Role.id).where(
                    Role.role == role
                ).scalar_subquery()
            )
        )
        return list(session.scalars(query).all())


def get_user_id_by_username(username: str) -> int | None:
    """
    Возвращает айди пользователя по его имени в базе.

    :param username: Имя юзера.
    :return: Айди юзера.
    """

    with create_session() as session:
        query = sa.Select(User.user_id).where(User.username == username)
        return session.scalar(query)


def get_full_lessons(lessons_date: date, grade: str) -> str | None:
    """
    Возвращает айди картинки расписания уроков для параллели.

    :param lessons_date: Дата.
    :param grade: 10 или 11.
    :return: Айди картинки или None.
    """

    with create_session() as session:
        query = sa.Select(FullLessons).where(
            FullLessons.date == lessons_date,
            FullLessons.grade == grade
        )
        lessons: FullLessons = session.scalar(query)
        return lessons.image if lessons else None


def get_class_lessons(
        lessons_date: date,
        class_: str
) -> str | None:
    """
    Возвращает айди картинки расписания уроков для класса.

    :param lessons_date: Дата.
    :param class_: (10 или 11) + (А, Б, В) .
    :return: Айди картинки или None.
    """

    with create_session() as session:
        query = sa.Select(ClassLessons).where(
            ClassLessons.date == lessons_date,
            ClassLessons.class_ == class_
        )
        lessons: ClassLessons = session.scalar(query)
        return lessons.image if lessons else None


def update_user(user_id: int, **params) -> None:
    """
    Обновление пользователя по айди.

    :param user_id: ТГ Айди юзера.
    :param params: Поле таблицы=значение, ...
    """

    with create_session(do_commit=True) as session:
        query = sa.update(User).where(
            User.user_id == user_id
        ).values(
            **params
        )
        session.execute(query)


def edit_meal_by_date(
        meal: str,
        new_menu: str,
        menu_date: date,
        edit_by: int
) -> None:
    """
    Обновляет приём пищи по названию и дате

    :param meal: Название приёма пищи на английском.
    :param new_menu: Новая версия.
    :param menu_date: Дата.
    :param edit_by: ТГ Айди того, кто меняет.
    """
    menu = get_menu_by_date(menu_date)
    db_id = get_user(edit_by).id

    meals = {
        meal: getattr(menu, meal, None) for meal in menu_eng_to_ru.keys()
    }
    meals[meal] = new_menu

    save_or_update_menu_in_db(
        menu_date=menu_date,
        edit_by=db_id,
        **meals
    )


def is_has_role(user_id: int, role: Roles | str) -> bool:
    """
    Имеет ли юзер роль.

    :param user_id: ТГ Айди юзера.
    :param role: Роль.
    :return: Тру или фэлс.
    """

    if isinstance(role, Enum):
        role = role.value

    with create_session() as session:
        role = get_role(role)
        user_query = sa.select(User).where(
            User.user_id == user_id,
        )
        user = session.scalar(user_query)
        return role in user.roles or any(
            user_role.id <= role.id for user_role in user.roles
        )


def remove_role_from_user(user_id: int, role: Roles | str) -> None:
    """
    Удаляет роль у юзера.

    :param user_id: ТГ Айди юзера.
    :param role: Его роль.
    """

    if isinstance(role, Roles):
        role = role.value

    with create_session(do_commit=True) as session:
        user_query = sa.Select(User).where(User.user_id == user_id)
        user = session.scalar(user_query)
        role_query = sa.select(Role).where(
            Role.role == role
        )
        role = session.scalar(role_query)
        try:
            user.roles.remove(role)
        except ValueError:
            pass


def add_role_to_user(user_id: int, role: Roles | str) -> None:
    """
    Добавляет роль юзеру.

    :param user_id: ТГ Айди юзера.
    :param role: Роль.
    """

    if isinstance(role, Roles):
        role = role.value

    with create_session(do_commit=True) as session:
        user_query = sa.Select(User).where(User.user_id == user_id)
        user = session.scalar(user_query)
        role_query = sa.select(Role).where(
            Role.role == role
        )
        role = session.scalar(role_query)
        user.roles.append(role)
