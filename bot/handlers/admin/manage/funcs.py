from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup

from bot.keyboards import (
    admins_list_keyboard,
    cancel_state_keyboard,
    check_admin_roles_keyboard,
    edit_roles_keyboard,
)
from shared.database.repository import UserRepository, UserRoleRepository
from shared.utils.enums import RoleEnum
from shared.utils.funcs import name_link
from shared.utils.phrases import YES
from shared.utils.states import EditingRoles
from shared.utils.translate import ROLES_TRANSLATE


async def admins_list_func(
    page: int,
    repo: "UserRoleRepository",
) -> tuple[str, "InlineKeyboardMarkup"]:
    """
    Обработчик кнопки "Список админов".

    :param page: Страница.
    :param repo: Репозиторий пользователей.
    :return: Сообщение и клавиатура пользователю.
    """
    admins = [
        (user.username, user.user_id) for user in await repo.get_users_with_any_roles()
    ]

    text = "👮‍♀️Список админов:"
    keyboard = admins_list_keyboard(admins, page)

    return text, keyboard


async def check_admin_roles_func(
    user_id: int,
    page: int,
    repo: "UserRepository",
) -> tuple[str, "InlineKeyboardMarkup"]:
    """
    Обработчик кнопки с юзернеймом админа в списке админов.

    :param user_id: Айди админа, которого смотрят.
    :param page: Страница, на которой был админ.
    :param repo: Репозиторий пользователей.
    :return: Сообщение и клавиатура пользователю.
    """
    user = await repo.get(user_id)
    roles = [role.role for role in user.roles]

    text = f"Телеграм - {name_link(user.username, user_id)}"
    keyboard = check_admin_roles_keyboard(user_id, page, roles)

    return text, keyboard


async def edit_role_directly_func(
    user_id: int,
    repo: "UserRepository",
    state: "FSMContext",
) -> tuple[str, "InlineKeyboardMarkup"]:
    """
    Обработчик кнопки изменения ролей при просмотре админа.

    :param user_id: Айди изменяемого пользователя.
    :param repo: Репозиторий пользователей.
    :param state: Состояние администратора.
    :return: Сообщение и клавиатура администратору.
    """
    username = (await repo.get(user_id)).username
    text, keyboard, _ = await edit_role_username_func(username, state, repo)
    return text, keyboard


async def edit_role_username_func(
    text: str,
    state: "FSMContext",
    repo: "UserRepository",
) -> tuple[str, "InlineKeyboardMarkup", int]:
    """
    Обработчик сообщения с юзернеймом, у которого хотят изменить роли.

    :param text: Сообщение пользователя.
    :param state: Состояние пользователя.
    :param repo: Репозиторий пользователей.
    :return: Сообщение, клавиатура администратору и айди первого сообщения бота.
    """
    username = text.split("/")[-1].lstrip("@")

    if not (user_ids := await repo.get_user_ids_by_username(username)):
        text = "Не могу найти у себя такого пользователя."
        return text, cancel_state_keyboard, -1

    # TODO: сделать обработку случая, когда в бд есть одинаковые юзернеймы
    if len(user_ids) > 1:
        pass

    user_id = user_ids[0]

    all_roles = RoleEnum.roles_which_can_be_edited()
    choosed_roles = [role.role for role in (await repo.get(user_id)).roles]
    await state.set_state(EditingRoles.roles)
    data = await state.update_data(
        user_id=user_id,
        username=username,
        all_roles=all_roles,
        choosed_roles=choosed_roles,
    )

    return (
        f"Выберите роли, которые будут у {name_link(username, user_id)}",
        edit_roles_keyboard(all_roles, choosed_roles),
        data.get("start_id", -1),
    )


async def edit_role_choose_role_func(
    role: str,
    state: "FSMContext",
) -> tuple[str, "InlineKeyboardMarkup"]:
    """
    Обработчик кнопок с ролями при редактировании ролей пользователя.

    :param role: Выбранная роль.
    :param state: Состояние пользователя.
    :return Сообщение, клавиатура пользователю и айди начального сообщения бота.
    """
    data = await state.get_data()
    all_roles: list[str] = data["all_roles"]
    choosed_roles: list[str] = data["choosed_roles"]
    user_id: int = data["user_id"]
    username: str = data["username"]

    if role in choosed_roles:
        choosed_roles.remove(role)
    else:
        choosed_roles.append(role)

    await state.update_data(choosed_roles=choosed_roles)

    return (
        f"Выберите роли, которые будут у {name_link(username, user_id)}",
        edit_roles_keyboard(all_roles, choosed_roles),
    )


async def edit_role_confirm_func(state: "FSMContext") -> str:
    """
    Обработчик кнопки "Подтвердить" при изменении ролей.

    :param state: Состояние пользователя.
    :return Сообщение, клавиатура пользователю и айди начального сообщения бота.
    """
    await state.set_state(EditingRoles.confirm)
    data = await state.get_data()
    user_id: int = data["user_id"]
    username: str = data["username"]
    choosed_roles: list[str] = data["choosed_roles"]

    foramtted_roles = (
        ", ".join(ROLES_TRANSLATE[role].capitalize() for role in choosed_roles)
        or "Нет ролей"
    )
    return (
        f"Вы уверены, что у {name_link(username, user_id)} будут роль(-и):\n"
        f"{foramtted_roles} ?"
    )


async def edit_role_confirm_sure_func(
    state: "FSMContext",
    repo: "UserRoleRepository",
) -> str:
    """
    Обработчик кнопки "Подтвердить" при подтверждении изменения ролей.

    :param state: Состояния администратора.
    :param repo: Доступ к базе данных.
    :return Сообщение администратору и айди начального сообщения бота.
    """
    data = await state.get_data()
    user_id: int = data["user_id"]
    choosed_roles: list[str] = data["choosed_roles"]

    await repo.remove_all_roles_from_user(user_id)
    for role in choosed_roles:
        await repo.add_role_to_user(user_id, role)

    return f"{YES} Успешно!"
