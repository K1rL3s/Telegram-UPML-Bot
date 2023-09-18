from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.filters import StateFilter

from bot.funcs.admin.admin_cafe_menu import (
    edit_cafe_menu_confirm_func,
    edit_cafe_menu_date_func,
    edit_cafe_menu_meal_func,
    edit_cafe_menu_text_func,
)
from bot.keyboards import (
    admin_panel_keyboard,
    cancel_state_keyboard,
    confirm_cancel_keyboard,
)
from bot.upml.save_cafe_menu import process_cafe_menu
from bot.utils.enums import AdminCallback
from bot.utils.datehelp import date_today, format_date
from bot.utils.states import EditingMenu

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext
    from aiogram.types import CallbackQuery, Message

    from bot.settings import Settings
    from bot.database.repository.repository import Repository


router = Router(name=__name__)


@router.callback_query(F.data == AdminCallback.AUTO_UPDATE_CAFE_MENU)
async def auto_update_cafe_menu_handler(
    callback: "CallbackQuery",
    settings: "Settings",
    repo: "Repository",
) -> None:
    """Обработчик кнопки "Загрузить меню".

    Загружает и обрабатывает PDF расписание еды с сайта лицея.
    """
    _, text = await process_cafe_menu(repo.menu, settings.other.TIMEOUT)

    await callback.message.edit_text(
        text=text,
        reply_markup=await admin_panel_keyboard(repo.user, callback.from_user.id),
    )


@router.callback_query(F.data == AdminCallback.EDIT_CAFE_MENU)
async def edit_cafe_menu_start_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
) -> None:
    """Обрабочтки кнопки "Изменить меню"."""
    text = f"""
Введите дату дня, меню которого хотите изменить в формате <b>ДД.ММ.ГГГГ</b>
Например, <code>{format_date(date_today())}</code>
""".strip()

    await state.set_state(EditingMenu.choose_date)
    await state.update_data(start_id=callback.message.message_id)

    await callback.message.edit_text(text=text, reply_markup=cancel_state_keyboard)


@router.message(StateFilter(EditingMenu.choose_date))
async def edit_cafe_menu_date_handler(
    message: "Message",
    state: "FSMContext",
) -> None:
    """Обработчик ввода даты для изменения меню."""
    text, keyboard, start_id = await edit_cafe_menu_date_func(message.text, state)

    await message.delete()
    await message.bot.edit_message_text(
        text=text,
        chat_id=message.chat.id,
        message_id=start_id,
        reply_markup=keyboard,
    )


@router.callback_query(StateFilter(EditingMenu.choose_meal))
async def edit_cafe_menu_meal_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
    repo: "Repository",
) -> None:
    """Обработчик кнопки с выбором приёма пищи для изменения."""
    text = await edit_cafe_menu_meal_func(callback.data, state, repo.menu)
    await callback.message.edit_text(text=text, reply_markup=cancel_state_keyboard)


@router.message(StateFilter(EditingMenu.writing))
async def edit_cafe_menu_text_handler(
    message: "Message",
    state: "FSMContext",
) -> None:
    """Обработчик сообщения с изменённой версией приёма пищи."""
    text, start_id = await edit_cafe_menu_text_func(
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


@router.callback_query(StateFilter(EditingMenu.writing))
async def edit_cafe_menu_confirm_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
    repo: "Repository",
) -> None:
    """Обработчик подтверждения изменения меню."""
    text, new_ids = await edit_cafe_menu_confirm_func(
        callback.from_user.id,
        state,
        repo.menu,
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
