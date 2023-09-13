from typing import TYPE_CHECKING

from bot.funcs.admin.admin import get_users_for_notify
from bot.keyboards import (
    cancel_state_keyboard,
    notify_for_class_keyboard,
    notify_for_grade_keyboard,
)
from bot.utils.consts import NOTIFIES_ENG_TO_RU
from bot.utils.enums import AdminCallback
from bot.utils.notify import do_admin_notifies
from bot.utils.states import DoNotify

if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram.types import InlineKeyboardMarkup
    from aiogram.fsm.context import FSMContext

    from bot.database.repository import UserRepository


async def notify_for_who_func(
    callback_data: str,
    message_id: int,
    state: "FSMContext",
) -> tuple[str, "InlineKeyboardMarkup"]:
    """
    Обработчик нажатия одной из кнопок уведомления в панели уведомлений.

    :param callback_data: Callback строка.
    :param message_id: Айди начального сообщения бота.
    :param state: Состояние пользователя.
    :return: Сообщение и клавиатура для пользователя.
    """
    if callback_data == AdminCallback.NOTIFY_FOR_GRADE:
        text = "Выберите, каким классам сделать уведомление"
        keyboard = notify_for_grade_keyboard
    elif callback_data == AdminCallback.NOTIFY_FOR_CLASS:
        text = "Выберите, какому классу сделать уведомление"
        keyboard = notify_for_class_keyboard
    else:
        notify_type = callback_data.replace(AdminCallback.DO_A_NOTIFY_FOR_, "")
        await state.set_state(DoNotify.writing)
        await state.set_data(
            {
                "start_id": message_id,
                # all, grade_10, grade_11, 10А, 10Б, 10В, 11А, 11Б, 11В
                "notify_type": notify_type,
            },
        )
        text = (
            f"Тип: <code>{NOTIFIES_ENG_TO_RU.get(notify_type, notify_type)}</code>\n"
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
    notify_type = data["notify_type"]

    messages_ids = data.get("messages_ids", [])
    messages_ids.append(message_id)
    await state.update_data(message_text=html_text, messages_ids=messages_ids)

    text = (
        f"Тип: <code>{NOTIFIES_ENG_TO_RU.get(notify_type, notify_type)}</code>\n"
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
    notify_type = data["notify_type"]
    message_text = data["message_text"]
    messages_ids = data["messages_ids"]
    await state.clear()

    users = await get_users_for_notify(repo, notify_type, is_news=True)
    await do_admin_notifies(
        bot,
        repo,
        message_text,
        users,
        user_id,
        NOTIFIES_ENG_TO_RU.get(notify_type, notify_type),
    )

    return "Рассылка завершена!", messages_ids
