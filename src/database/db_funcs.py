from datetime import date
from enum import Enum
from typing import Any, Type

import sqlalchemy as sa
from loguru import logger

from src.database.models.base_model import BaseModel
from src.database.models.class_lessons import ClassLessons
from src.database.models.full_lessons import FullLessons
from src.database.models.laundries import Laundry
from src.database.models.menus import Menu
from src.database.models.roles import Role
from src.database.models.settings import Settings
from src.database.models.users import User
from src.database.db_session import create_session
from src.utils.consts import Roles, menu_eng_to_ru
from src.utils.datehelp import datetime_now


def save_new_user(user_id: int, username: str) -> None:
    """
    Сохраняет пользователя в базе данных
    или обновляет его статус ``is_active``, никнейм,
    создаёт Settings и Laundry.

    :param user_id: Айди юзера.
    :param username: Имя пользователя.
    """

    with create_session(do_commit=True) as session:
        user_query = sa.select(User).where(User.user_id == user_id)
        user: User = session.scalar(user_query)

        if user and (not user.is_active or user.username != username):
            user.is_active = True
            user.username = username
        elif not user:
            user = User(user_id=user_id, username=username)
            session.add(user)
            logger.info(f'Новый пользователь {user}')

    save_or_update_settings(user_id)
    save_or_update_laundry(user_id)


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
    :param edit_by: Кем редактируется, ТГ Айди, 0 - автоматически.
    """

    with create_session(do_commit=True) as session:
        user = get_user(edit_by)

        find_query = sa.select(Menu).where(Menu.date == menu_date)

        if menu := session.scalar(find_query):
            menu.breakfast = menu.breakfast or breakfast
            menu.lunch = menu.lunch or lunch
            menu.dinner = menu.dinner or dinner
            menu.snack = menu.snack or snack
            menu.supper = menu.supper or supper
            menu.edit_by = menu.edit_by or (user.id if edit_by else 0)
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
        find_query = sa.select(model).where(
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


def save_or_update_laundry(
        user_id: int,
        **kwargs
) -> Laundry:
    """
    Сохраняет или обновляет уведомление о стирке/сушке.

    :param user_id: ТГ Айди.
    :param kwargs: Поле таблицы=значение.
    :return: Модель Laundry.
    """

    with create_session(do_commit=True) as session:
        db_user_id_query = sa.select(User.id).where(User.user_id == user_id)
        db_user_id = session.scalar(db_user_id_query)

        # noinspection PyTypeChecker
        query = sa.select(Laundry).where(Laundry.user_id == db_user_id)

        if laundry := session.scalar(query):
            for k, v in kwargs.items():
                setattr(laundry, k, v)
        else:
            laundry = Laundry(user_id=db_user_id)
            session.add(laundry)

    return laundry


def save_or_update_settings(
        user_id: int,
        **kwargs
) -> None:
    """
    Создаёт или обнолвяет настройки пользователя.

    :param user_id: ТГ Айди.
    :param kwargs: Поле таблицы=значение.
    :return: модель Settings.
    """
    with create_session(do_commit=True) as session:
        db_user_id_query = sa.select(User.id).where(User.user_id == user_id)
        db_user_id = session.scalar(db_user_id_query)

        # noinspection PyTypeChecker
        query = sa.select(Settings).where(Settings.user_id == db_user_id)

        if settings := session.scalar(query):
            for k, v in kwargs.items():
                setattr(settings, k, v)
        else:
            settings = Settings(
                user_id=db_user_id,
                **kwargs
            )
            session.add(settings)


def get_menu_by_date(menu_date: date) -> Menu | None:
    """
    Возвращает меню на день по дате.

    :param menu_date: Дата запрашеваемого меню.
    :return: Модель Menu.
    """

    with create_session() as session:
        query = sa.select(Menu).where(Menu.date == menu_date)
        return session.scalar(query)


def get_users_by_conditions(
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

    with create_session() as session:
        conditions = []
        for attr, value in values:
            try:
                conditions.append(getattr(Settings, attr) == value)
            except AttributeError:
                conditions.append(getattr(User, attr) == value)

        if or_mode:
            find_query = sa.select(User).join(Settings).where(
                sa.or_(*conditions)
            )
        else:
            find_query = sa.select(User).join(Settings).where(
                sa.and_(*conditions)
            )

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
        query = sa.select(User.user_id).where(User.username == username)
        return session.scalar(query)


def get_full_lessons(lessons_date: date, grade: str) -> str | None:
    """
    Возвращает айди картинки расписания уроков для параллели.

    :param lessons_date: Дата.
    :param grade: 10 или 11.
    :return: Айди картинки или None.
    """

    with create_session() as session:
        query = sa.select(FullLessons).where(
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
        query = sa.select(ClassLessons).where(
            ClassLessons.date == lessons_date,
            ClassLessons.class_ == class_
        )
        lessons: ClassLessons = session.scalar(query)
        return lessons.image if lessons else None


def _get_model(
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

    with create_session() as session:
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

        return session.scalar(query)


def get_user(user_id: int) -> User | None:
    return _get_model(User, user_id)


def get_settings(user_id: int) -> Settings:
    return _get_model(Settings, user_id, do_subquery=True)


def get_laundry(user_id: int) -> Laundry:
    return _get_model(Laundry, user_id, do_subquery=True)


def get_expired_laundries() -> list[Laundry]:
    """
    Возвращает список моделей Laundry, у которых пришло время для уведомления.

    :return: Список из Laundry.
    """

    with create_session() as session:
        # noinspection PyTypeChecker
        query = sa.select(Laundry).where(
            Laundry.is_active == 1,
            Laundry.end_time <= datetime_now()
        )

        return list(session.scalars(query).all())


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

    meals = {
        meal: getattr(menu, meal, None) for meal in menu_eng_to_ru.keys()
    }
    meals[meal] = new_menu

    save_or_update_menu_in_db(
        menu_date=menu_date,
        edit_by=edit_by,
        **meals
    )


def is_has_any_role(user_id: int, roles: list[Roles | str]) -> bool:
    """
    Имеет ли юзер хотя бы одну роль из переданных.

    :param user_id: ТГ Айди юзера.
    :param roles: Список ролей.
    :return: Тру или фэлс.
    """

    with create_session() as session:
        user_query = sa.select(User).where(User.user_id == user_id)
        user = session.scalar(user_query)
        if user is None:
            return False

        role_names = [
            role.value if isinstance(role, Enum) else role
            for role in roles
        ]
        return any(role.role in role_names for role in user.roles)


def remove_role_from_user(user_id: int, role: Roles | str) -> None:
    """
    Удаляет роль у юзера.

    :param user_id: ТГ Айди юзера.
    :param role: Его роль.
    """

    if isinstance(role, Roles):
        role = role.value

    with create_session(do_commit=True) as session:
        user_query = sa.select(User).where(User.user_id == user_id)
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
        user_query = sa.select(User).where(User.user_id == user_id)
        user = session.scalar(user_query)
        role_query = sa.select(Role).where(
            Role.role == role
        )
        role = session.scalar(role_query)
        user.roles.append(role)
