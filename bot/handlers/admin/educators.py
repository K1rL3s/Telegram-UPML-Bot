from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.filters import StateFilter

from bot.callbacks import AdminEditData, StateData
from bot.funcs.admin.admin_educators import (
    edit_educators_confirm_func,
    edit_educators_date_func,
    edit_educators_text_func,
)
from bot.keyboards import cancel_state_keyboard, confirm_cancel_keyboard
from bot.keyboards.admin.admin import admin_panel_keyboard
from bot.utils.enums import Actions, Menus
from bot.utils.datehelp import date_today, format_date
from bot.utils.states import EditingEducators

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext
    from aiogram.types import CallbackQuery, Message

    from bot.database.repository.repository import Repository


router = Router(name=__name__)


@router.callback_query(AdminEditData.filter(F.menu == Menus.EDUCATORS))
async def edit_educators_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
) -> None:
    """Обработчик ввода даты для изменения расписания воспитателей."""
    text = f"""
Введите дату дня, расписание которого хотите изменить в формате <b>ДД.ММ.ГГГГ</b>
Например, <code>{format_date(date_today())}</code>
""".strip()

    await state.set_state(EditingEducators.choose_date)
    await state.update_data(start_id=callback.message.message_id)

    await callback.message.edit_text(text=text, reply_markup=cancel_state_keyboard)


@router.message(StateFilter(EditingEducators.choose_date))
async def edit_educators_date_handler(
    message: "Message",
    state: "FSMContext",
    repo: "Repository",
) -> None:
    """Обработчик ввода даты для изменения расписания воспитателей."""
    text, start_id = await edit_educators_date_func(message.text, state, repo.educators)

    await message.delete()  # ?
    await message.bot.edit_message_text(
        text=text,
        chat_id=message.chat.id,
        message_id=start_id,
        reply_markup=cancel_state_keyboard,
    )


@router.message(StateFilter(EditingEducators.writing))
async def edit_educators_text_handler(
    message: "Message",
    state: "FSMContext",
) -> None:
    """Обработчик сообщения с изменённым расписанием воспитателей."""
    text, start_id = await edit_educators_text_func(
        message.html_text,
        message.message_id,
        state,
    )

    await message.bot.edit_message_text(
        text=text,
        chat_id=message.chat.id,
        message_id=start_id,
        reply_markup=confirm_cancel_keyboard,
    )


@router.callback_query(
    StateFilter(EditingEducators.writing),
    StateData.filter(F.action == Actions.CONFIRM),
)
async def edit_educators_confirm_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
    repo: "Repository",
) -> None:
    """Обработчик подтверждения изменения расписания воспитетелей."""
    text, new_ids = await edit_educators_confirm_func(
        callback.from_user.id,
        state,
        repo.educators,
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=await admin_panel_keyboard(repo.user, callback.from_user.id),
    )

    for new_id in new_ids:
        await callback.bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=new_id,
        )
