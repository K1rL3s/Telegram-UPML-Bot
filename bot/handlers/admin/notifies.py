from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.filters import StateFilter

from bot.callbacks import DoNotifyData, OpenMenu, StateData
from bot.funcs.admin.admin_notifies import (
    notify_confirm_func,
    notify_for_who_func,
    notify_message_func,
)
from bot.keyboards import (
    admin_panel_keyboard,
    confirm_cancel_keyboard,
    notify_panel_keyboard,
)
from bot.utils.enums import Actions, Menus
from bot.utils.states import DoNotify

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext
    from aiogram.types import CallbackQuery, Message

    from bot.database.repository.repository import Repository


router = Router(name=__name__)


@router.callback_query(OpenMenu.filter(F.menu == Menus.NOTIFY))
async def notify_panel_handler(callback: "CallbackQuery") -> None:
    """Обработчик кнопки "Уведомление"."""
    text = """
Привет! Я - панель уведомлений.

<b>Всем</b> - для всех пользователей.
<b>Поток</b> - для 10 или 11 классов.
<b>Класс</b> - для конкретного класса.
""".strip()

    await callback.message.edit_text(text=text, reply_markup=notify_panel_keyboard)


@router.callback_query(DoNotifyData.filter())
async def notify_for_who_handler(
    callback: "CallbackQuery",
    callback_data: "DoNotifyData",
    state: "FSMContext",
) -> None:
    """Обработчик нажатия одной из кнопок уведомления в панели уведомлений."""
    text, keyboard = await notify_for_who_func(
        callback_data.notify_type,
        callback_data.for_who,
        callback.message.message_id,
        state,
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.message(StateFilter(DoNotify.writing))
async def notify_message_handler(
    message: "Message",
    state: "FSMContext",
) -> None:
    """Обработчик сообщения с текстом для рассылки."""
    text, start_id = await notify_message_func(
        message.html_text,
        message.message_id,
        state,
    )
    await message.bot.edit_message_text(
        text=text,
        message_id=start_id,
        chat_id=message.chat.id,
        reply_markup=confirm_cancel_keyboard,
    )


@router.callback_query(
    StateData.filter(F.action == Actions.CONFIRM),
    StateFilter(DoNotify.writing),
)
async def notify_confirm_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
    repo: "Repository",
) -> None:
    """Обработчик подтверждения отправки рассылки."""
    text, messages_ids = await notify_confirm_func(
        callback.from_user.id,
        callback.bot,
        state,
        repo.user,
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=await admin_panel_keyboard(repo.user, callback.from_user.id),
    )

    for message_id in messages_ids:
        await callback.bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=message_id,
        )
