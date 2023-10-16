from typing import TYPE_CHECKING

from bot.keyboards import (
    admins_list_keyboard,
    cancel_state_keyboard,
    check_admin_keyboard,
    confirm_cancel_keyboard,
)
from bot.utils.enums import Roles
from bot.utils.funcs import name_link, username_by_user_id
from bot.utils.states import AddingNewAdmin

if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram.fsm.context import FSMContext
    from aiogram.types import InlineKeyboardMarkup

    from bot.database.repository.repository import Repository
    from bot.database.repository import UserRepository


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


async def admin_add_username_func(
    text: str,
    state: "FSMContext",
    repo: "UserRepository",
) -> tuple[str, "InlineKeyboardMarkup"]:
    """
    Обработчик сообщения с юзернеймом админа, которого хотят добавить.

    :param text: Сообщение пользователя.
    :param state: Состояние пользователя.
    :param repo: Репозиторий пользователей.
    :return: Сообщение и клавиатура пользователю.
    """
    username = text.split("/")[-1].lstrip("@")

    if (user_id := await repo.get_user_id_by_username(username)) is None:
        text = "Не могу найти у себя такого пользователя."
        return text, cancel_state_keyboard

    await state.update_data(user_id=user_id)
    await state.set_state(AddingNewAdmin.confirm)

    text = f"Добавить в админы {name_link(username, user_id)}?"
    return text, confirm_cancel_keyboard


async def admin_add_confirm_func(
    state: "FSMContext",
    repo: "Repository",
) -> str:
    """
    Обработчик кнопки "Подтвердить" при добавлении админа.

    :param state: Состояние пользователя.
    :param repo: Доступ к базе данных.
    :return: Сообщение пользователю.
    """
    user_id = (await state.get_data())["user_id"]
    await repo.add_role_to_user(user_id, Roles.ADMIN)
    return "Успешно!"


async def admin_check_func(
    user_id: int,
    page: int,
    bot: "Bot",
) -> tuple[str, "InlineKeyboardMarkup"]:
    """
    Обработчик кнопки с юзернеймом админа в списке админов.

    :param user_id: Айди админа, которого смотрят.
    :param page: Страница, на которой был админ.
    :param bot: ТГ Бот.
    :return: Сообщение и клавиатура пользователю.
    """
    username = await username_by_user_id(bot, user_id)

    text = f"Телеграм - {name_link(username, user_id)}"
    keyboard = check_admin_keyboard(user_id, page, is_sure=False)

    return text, keyboard


async def admin_remove_func(
    user_id: int,
    is_sure: bool,
    page: int,
    bot: "Bot",
    repo: "Repository",
) -> tuple[str, "InlineKeyboardMarkup"]:
    """
    Обработчик кнопкок "Снять роль админа" и "Точно снять роль".

    :param user_id: Айди админа.
    :param is_sure: Точно ли удалить админа.
    :param page: Страница, на которой был админ.
    :param bot: ТГ Бот.
    :param repo: Доступ к базе данных.
    :return: Сообщение и клавиатура пользователю.
    """
    if is_sure:
        await repo.remove_role_from_user(user_id, Roles.ADMIN)

        return await admins_list_func(
            page,
            repo.user,
        )

    username = await username_by_user_id(bot, user_id)

    text = f"Вы точно хотите удалить из админов {name_link(username, user_id)}?"
    keyboard = check_admin_keyboard(user_id, page, is_sure=True)

    return text, keyboard
