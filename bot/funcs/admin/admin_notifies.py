from typing import TYPE_CHECKING

from bot.funcs.admin.admin import get_users_for_notify
from bot.keyboards import (
    cancel_state_keyboard,
    notify_for_class_keyboard,
    notify_for_grade_keyboard,
)
from bot.utils.consts import NOTIFIES_ENG_TO_RU
from bot.utils.enums import NotifyTypes
from bot.utils.notify import do_admin_notifies
from bot.utils.states import DoNotify

if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram.types import InlineKeyboardMarkup
    from aiogram.fsm.context import FSMContext

    from bot.database.repository import UserRepository


async def notify_for_who_func(
    notify_type: str,
    for_who: str,
    message_id: int,
    state: "FSMContext",
) -> tuple[str, "InlineKeyboardMarkup"]:
    """
    Обработчик нажатия одной из кнопок уведомления в панели уведомлений.

    :param notify_type: Тип уведомления.
    :param for_who: Для кого уведомление.
    :param message_id: Айди начального сообщения бота.
    :param state: Состояние пользователя.
    :return: Сообщение и клавиатура для пользователя.
    """
    if notify_type == NotifyTypes.GRADE:
        text = "Выберите, каким классам сделать уведомление"
        keyboard = notify_for_grade_keyboard
    elif notify_type == NotifyTypes.CLASS:
        text = "Выберите, какому классу сделать уведомление"
        keyboard = notify_for_class_keyboard
    else:
        await state.set_state(DoNotify.writing)
        await state.set_data(
            {
                "start_id": message_id,
                # all, grade_10, grade_11, 10А, 10Б, 10В, 11А, 11Б, 11В
                "for_who": for_who,
            },
        )
        text = (
            f"Тип: <code>{NOTIFIES_ENG_TO_RU.get(for_who, for_who)}</code>\n"
            "Напишите сообщение, которое будет в уведомлении"
        )
        keyboard = cancel_state_keyboard

    return text, keyboard


async def notify_message_func(
    html_text: str,
    message_id: int,
    state: "FSMContext",
) -> tuple[str, int]:
    """
    Обработчик сообщения с текстом для рассылки.

    :param html_text: Сообщение пользователя в html'е.
    :param message_id: Айди сообщения юзера.
    :param state: Состояние пользователя.
    :return: Сообщение и айди начального сообщения бота.
    """
    data = await state.get_data()
    start_id = data["start_id"]
    for_who = data["for_who"]

    messages_ids = data.get("messages_ids", [])
    messages_ids.append(message_id)
    await state.update_data(message_text=html_text, messages_ids=messages_ids)

    text = (
        f"Тип: <code>{NOTIFIES_ENG_TO_RU.get(for_who, for_who)}</code>\n"
        f"Сообщение:\n{html_text}\n\n"
        "Для отправки нажмите кнопку. Если хотите изменить, "
        "отправьте сообщение повторно."
    )

    return text, start_id


async def notify_confirm_func(
    user_id: int,
    bot: "Bot",
    state: "FSMContext",
    repo: "UserRepository",
) -> tuple[str, list[int]]:
    """
    Обработчик подтверждения отправки рассылки.

    :param user_id: ТГ Айди.
    :param bot: ТГ Бот.
    :param state: Состояние пользователя.
    :param repo: Репозиторий пользователей.
    :return: Сообщение пользователю и айдишники его сообщений с изменениями.
    """
    data = await state.get_data()
    for_who = data["for_who"]
    message_text = data["message_text"]
    messages_ids = data["messages_ids"]
    await state.clear()

    users = await get_users_for_notify(repo, for_who, is_news=True)
    await do_admin_notifies(
        bot,
        repo,
        message_text,
        users,
        user_id,
        NOTIFIES_ENG_TO_RU.get(for_who, for_who),
    )

    return "Рассылка завершена!", messages_ids
