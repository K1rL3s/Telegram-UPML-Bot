from typing import TYPE_CHECKING

from bot.keyboards import (
    admins_list_keyboard,
    cancel_state_keyboard,
    check_admin_keyboard,
    confirm_cancel_keyboard,
    edit_roles_keyboard,
    roles_actions_keyboard,
)
from bot.utils.enums import Actions, Roles
from bot.utils.funcs import name_link, username_by_user_id
from bot.utils.states import EditingRoles
from bot.utils.translate import ACTIONS_TRANSLATE, ROLES_TRANSLATE


if TYPE_CHECKING:
    from aiogram import Bot
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


async def admin_check_func(
    user_id: int,
    page: int,
    bot: "Bot",
    repo: "UserRepository",
) -> tuple[str, "InlineKeyboardMarkup"]:
    """
    Обработчик кнопки с юзернеймом админа в списке админов.

    :param user_id: Айди админа, которого смотрят.
    :param page: Страница, на которой был админ.
    :param bot: ТГ Бот.
    :param repo: Репозиторий пользователей.
    :return: Сообщение и клавиатура пользователю.
    """
    username = await username_by_user_id(bot, user_id)
    roles = [role.role for role in (await repo.get(user_id)).roles]

    text = f"Телеграм - {name_link(username, user_id)}"
    keyboard = check_admin_keyboard(user_id, page, roles)

    return text, keyboard


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
    await state.update_data(user_id=user_id, username=username)

    text = f"Что будем делать с ролями {name_link(username, user_id)}?"
    return text, roles_actions_keyboard


async def edit_role_action_func(
    action: str,
    state: "FSMContext",
    user_repo: "UserRepository",
    role_repo: "RoleRepository",
) -> tuple[str, "InlineKeyboardMarkup"]:
    """
    Обработчик кнопок действия с ролями (добавить или удалить).

    :param action: Добавить или удалить.
    :param state: Состояние пользователя.
    :param user_repo: Репозиторий пользователей.
    :param role_repo: Репозиторий пользователей.
    :return: Сообщение и клавиатура пользователю.
    """
    await state.set_state(EditingRoles.role)
    data = await state.update_data(action=action)
    user_id = data["user_id"]
    username = data["username"]

    user_roles = [role.role for role in (await user_repo.get(user_id)).roles]

    roles: list[str] = []
    if action == Actions.ADD:
        roles = [role.role for role in await role_repo.get_all()]
        for role in user_roles:
            if role in roles:
                roles.remove(role)
    elif action == Actions.REMOVE:
        roles = user_roles

    return (
        f"Выберите роль, "
        f"которую надо {ACTIONS_TRANSLATE[action]} {name_link(username, user_id)}",
        edit_roles_keyboard(roles, action),
    )


async def edit_role_choose_role_func(
    role: str,
    state: "FSMContext",
) -> tuple[str, "InlineKeyboardMarkup"]:
    """
    Обработчик кнопок с ролями при редактировании ролей пользователя.

    :param role: Выбранная роль.
    :param state: Состояние пользователя.
    :return Сообщение и клавиатура пользователю.
    """
    await state.set_state(EditingRoles.confirm)
    data = await state.update_data(role=role)
    action = data["action"]
    username = data["username"]
    user_id = data["user_id"]

    return (
        f"Вы уверены, что хотите {ACTIONS_TRANSLATE[action]} "
        f'роль "{ROLES_TRANSLATE[role].capitalize()}" {name_link(username, user_id)}?',
        confirm_cancel_keyboard,
    )


async def edit_role_confirm_func(
    state: "FSMContext",
    repo: "Repository",
) -> str:
    """
    Обработчик кнопки "Подтвердить" при изменении ролей.

    :param state: Состояние пользователя.
    :param repo: Доступ к базе данных.
    :return: Сообщение пользователю.
    """
    data = await state.get_data()
    action = data["action"]
    user_id = data["user_id"]
    role = data["role"]

    if action == Actions.ADD:
        await repo.add_role_to_user(user_id, role)
    elif action == Actions.REMOVE:
        await repo.remove_role_from_user(user_id, role)

    return "Успешно!"
