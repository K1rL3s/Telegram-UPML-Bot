from datetime import date
from enum import Enum

import sqlalchemy as sa

from src.database.models.class_lessons import ClassLessons
from src.database.models.full_lessons import FullLessons
from src.database.models.menus import Menu
from src.database.models.roles import Role
from src.database.models.users import User
from src.database.db_session import create_session
from src.utils.consts import Roles


def save_user_or_update_status(user_id: int, username: str) -> None:
    """
    Сохраняет пользователя в базе данных
    или обновляет его статус ``is_active``.

    :param user_id: Айди юзера.
    :param username: Имя пользователя.
    """

    with create_session(do_commit=True) as session:
        query = sa.Select(User).where(User.user_id == user_id)
        user: User = session.scalar(query)

        if user and (not user.is_active or not user.username):
            user.is_active = True
            user.username = username
        elif not user:
            user = User(user_id=user_id, username=username)
            session.add(user)


def save_or_update_menu_in_db(
        menu_date: date,
        breakfast: str,
        lunch: str,
        dinner: str,
        snack: str,
        supper: str,
) -> None:
    """
    Сохраняет или обновляет меню для определённой даты.

    :param menu_date: Дата меня.
    :param breakfast: Завтрак.
    :param lunch: Второй завтрак.
    :param dinner: Обед.
    :param snack: Полдник.
    :param supper: Ужин.
    """

    with create_session(do_commit=True) as session:
        find_query = sa.Select(Menu).where(Menu.date == menu_date)
        if session.scalar(find_query):
            delete_query = sa.Delete(Menu).where(Menu.date == menu_date)
            session.execute(delete_query)

        menu = Menu(
            date=menu_date,
            breakfast=breakfast,
            lunch=lunch,
            dinner=dinner,
            snack=snack,
            supper=supper
        )
        session.add(menu)


def save_or_update_full_lessons(
        image: str,
        lessons_date: date,
        grade: int,
) -> None:
    """
    Сохраняет или обновляет уроки для паралелли.

    :param image: Айди изображения.
    :param lessons_date: Дата.
    :param grade: 10 или 11.
    """

    with create_session(do_commit=True) as session:
        find_query = sa.Select(FullLessons).where(
            FullLessons.date == lessons_date,
            FullLessons.grade == grade
        )
        if session.scalar(find_query):
            delete_query = sa.Delete(FullLessons).where(
                FullLessons.date == lessons_date,
                FullLessons.grade == grade
            )
            session.execute(delete_query)

        lessons = FullLessons(
            date=lessons_date,
            grade=grade,
            image=image
        )
        session.add(lessons)


def save_or_update_class_lessons(
        image: str,
        lessons_date: date,
        grade: int,
        letter: str
) -> None:
    """
    Сохраняет или обновляет уроки для класса.

    :param image: Айди изображения.
    :param lessons_date: Дата.
    :param grade: 10 или 11.
    :param letter: А, Б, В.
    """

    with create_session(do_commit=True) as session:
        find_query = sa.Select(ClassLessons).where(
            ClassLessons.date == lessons_date,
            ClassLessons.letter == letter,
            ClassLessons.grade == grade
        )
        if session.scalar(find_query):
            delete_query = sa.Delete(ClassLessons).where(
                ClassLessons.date == lessons_date,
                ClassLessons.letter == letter,
                ClassLessons.grade == grade
            )
            session.execute(delete_query)

        lessons = ClassLessons(
            date=lessons_date,
            grade=grade,
            letter=letter,
            image=image,
        )
        session.add(lessons)


def get_menu_by_date(menu_date: date) -> Menu:
    """
    Возвращает меню на день по дате.

    :param menu_date: Дата запрашеваемого меню.
    :return: Модель Menu.
    """

    with create_session() as session:
        query = sa.Select(Menu).where(Menu.date == menu_date)
        return session.scalar(query)


def get_user(user_id: int) -> User:
    """
    Возвращает модель User по айди пользователя.

    :param user_id: Айди юзера.
    :return: Модель User.
    """

    with create_session() as session:
        query = sa.Select(User).where(User.user_id == user_id)
        return session.scalar(query)


def get_role(role: Roles | str) -> Role:
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


def get_full_lessons(
        lessons_date: date,
        grade: int
) -> str | None:
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
        grade: int,
        letter: str
) -> str | None:
    """
    Возвращает айди картинки расписания уроков для класса.

    :param lessons_date: Дата.
    :param grade: 10 или 11.
    :param letter: А, Б, В.
    :return: Айди картинки или None.
    """

    with create_session() as session:
        query = sa.Select(ClassLessons).where(
            ClassLessons.date == lessons_date,
            ClassLessons.grade == grade,
            ClassLessons.letter == letter
        )
        lessons: ClassLessons = session.scalar(query)
        return lessons.image if lessons else None


def update_user(user_id: int, **params) -> None:
    """
    Обновление пользователя по айди.

    :param user_id: Айди юзера.
    :param params: Поле таблицы=значение, ...
    """

    with create_session(do_commit=True) as session:
        query = sa.update(User).where(
            User.user_id == user_id
        ).values(
            **params
        )
        session.execute(query)


def is_has_role(user_id: int, role: Roles | str) -> bool:
    """
    Имеет ли юзер роль.

    :param user_id: Айди юзера.
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

    :param user_id: Айди юзера.
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

    :param user_id: Айди юзера.
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
