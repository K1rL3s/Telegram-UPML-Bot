from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks import AdminEditMenu, InStateData
from bot.filters import HasEducatorsRole
from bot.keyboards import (
    admin_panel_keyboard,
    cancel_state_keyboard,
    confirm_cancel_keyboard,
)
from shared.database.repository.repository import Repository
from shared.utils.enums import Action, BotMenu
from shared.utils.states import EditingEducators

from .funcs import (
    edit_educators_confirm_func,
    edit_educators_date_func,
    edit_educators_start_func,
    edit_educators_text_func,
)

router = Router(name=__name__)
router.message.filter(HasEducatorsRole())
router.callback_query.filter(HasEducatorsRole())


@router.callback_query(AdminEditMenu.filter(F.menu == BotMenu.EDUCATORS))
async def edit_educators_start_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
) -> None:
    """Обработчик кнопки "Изменить меню"."""
    text = await edit_educators_start_func(callback.message.message_id, state)
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


@router.message(StateFilter(EditingEducators.write))
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
    StateFilter(EditingEducators.write),
    InStateData.filter(F.action == Action.CONFIRM),
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
