from typing import TYPE_CHECKING

from bot.keyboards import (
    admins_list_keyboard,
    cancel_state_keyboard,
    check_admin_roles_keyboard,
    edit_roles_keyboard,
    roles_actions_keyboard,
)
from bot.utils.enums import Actions, Roles
from bot.utils.funcs import name_link
from bot.utils.states import EditingRoles
from bot.utils.translate import ACTIONS_TRANSLATE, ROLES_TRANSLATE


if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext
    from aiogram.types import InlineKeyboardMarkup

    from bot.database.repository.repository import Repository
    from bot.database.repository import RoleRepository, UserRepository


async def admins_list_func(
    page: int,
    repo: "UserRepository",
) -> tuple[str, "InlineKeyboardMarkup"]:
    """
    Обработчик кнопки "Список админов".

    :param page: Страница.
    :param repo: Репозиторий пользователей.
    :return: Сообщение и клавиатура пользователю.
    """
    admins = [
        (user.username, user.user_id) for user in await repo.get_with_role(Roles.ADMIN)
    ]

    text = "Список админов:"
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

    await state.set_state(EditingRoles.action)
    await state.update_data(
        user_id=user_id,
        username=username,
    )
    return await edit_role_username_func(username, state, repo)


async def edit_role_username_func(
    text: str,
    state: "FSMContext",
    repo: "UserRepository",
) -> tuple[str, "InlineKeyboardMarkup"]:
    """
    Обработчик сообщения с юзернеймом, у которого хотят изменить роли.

    :param text: Сообщение пользователя.
    :param state: Состояние пользователя.
    :param repo: Репозиторий пользователей.
    :return: Сообщение и клавиатура пользователю.
    """
    username = text.split("/")[-1].lstrip("@")

    if (user_id := await repo.get_user_id_by_username(username)) is None:
        text = "Не могу найти у себя такого пользователя."
        return text, cancel_state_keyboard

    await state.set_state(EditingRoles.action)
    await state.update_data(user_id=user_id, username=username, roles=[])

    text = f"Что будем делать с ролями {name_link(username, user_id)}?"
    return text, roles_actions_keyboard


async def edit_role_action_func(
    action: str,
    message_id: int,
    state: "FSMContext",
    user_repo: "UserRepository",
    role_repo: "RoleRepository",
) -> tuple[str, "InlineKeyboardMarkup"]:
    """
    Обработчик кнопок действия с ролями (добавить или удалить).

    :param action: Добавить или удалить.
    :param message_id: Айди сообщения бота.
    :param state: Состояние пользователя.
    :param user_repo: Репозиторий пользователей.
    :param role_repo: Репозиторий пользователей.
    :return: Сообщение и клавиатура пользователю.
    """
    await state.set_state(EditingRoles.roles)
    data = await state.get_data()
    user_id: int = data["user_id"]
    username: str = data["username"]

    user_roles = [role.role for role in (await user_repo.get(user_id)).roles]

    if action == Actions.ADD:
        all_roles = [role.role for role in await role_repo.get_all()]
        for role in user_roles:
            if role in all_roles:
                all_roles.remove(role)
    else:  # action == Actions.REMOVE
        all_roles = user_roles

    await state.update_data(
        start_id=message_id,
        action=action,
        all_roles=all_roles,
        choosed_roles=[],
    )

    return (
        "Выберите роли, которые надо "
        f"{ACTIONS_TRANSLATE[action]} {name_link(username, user_id)}",
        edit_roles_keyboard(all_roles, [], action),
    )


async def edit_role_choose_role_func(
    role: str,
    state: "FSMContext",
) -> tuple[str, "InlineKeyboardMarkup", int]:
    """
    Обработчик кнопок с ролями при редактировании ролей пользователя.

    :param role: Выбранная роль.
    :param state: Состояние пользователя.
    :return Сообщение, клавиатура пользователю и айди начального сообщения бота.
    """
    data = await state.get_data()
    start_id: int = data["start_id"]
    action: str = data["action"]
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
        "Выберите роли, которые надо "
        f"{ACTIONS_TRANSLATE[action]} {name_link(username, user_id)}",
        edit_roles_keyboard(all_roles, choosed_roles, action),
        start_id,
    )


async def edit_role_confirm_func(
    state: "FSMContext",
) -> tuple[str, int]:
    """
    Обработчик кнопки "Подтвердить" при изменении ролей.

    :param state: Состояние пользователя.
    :return Сообщение, клавиатура пользователю и айди начального сообщения бота.
    """
    await state.set_state(EditingRoles.confirm)
    data = await state.get_data()
    start_id: int = data["start_id"]
    action: str = data["action"]
    user_id: int = data["user_id"]
    username: str = data["username"]
    choosed_roles: list[str] = data["choosed_roles"]

    foramtted_roles = ", ".join(
        ROLES_TRANSLATE[role].capitalize() for role in choosed_roles
    )
    return (
        f"Вы уверены, что хотите {ACTIONS_TRANSLATE[action]} "
        f'роль(-и) "{foramtted_roles}" {name_link(username, user_id)}?',
        start_id,
    )


async def edit_role_confirm_sure_func(
    state: "FSMContext",
    repo: "Repository",
) -> tuple[str, int]:
    """
    Обработчик кнопки "Подтвердить" при подтверждении изменения ролей.

    :param state: Состояния администратора.
    :param repo: Доступ к базе данных.
    :return Сообщение администратору и айди начального сообщения бота.
    """
    data = await state.get_data()
    start_id: int = data["start_id"]
    action: str = data["action"]
    user_id: int = data["user_id"]
    choosed_roles: list[str] = data["choosed_roles"]

    if action == Actions.ADD:
        crud = repo.add_role_to_user
    else:
        crud = repo.remove_role_from_user

    for role in choosed_roles:
        await crud(user_id, role)

    return "Успешно!", start_id
