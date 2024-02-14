from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks import AdminEditMenu, EditMeal, InStateData
from bot.filters import HasCafeMenuRole
from bot.keyboards import (
    admin_panel_keyboard,
    cancel_state_keyboard,
    confirm_cancel_keyboard,
)
from shared.core.settings import Settings
from shared.database.repository.repository import Repository
from shared.upml.cafe_menu import process_cafe_menu
from shared.utils.enums import Action, BotMenu, Meal
from shared.utils.states import EditingMenu

from .funcs import (
    edit_cafe_menu_confirm_func,
    edit_cafe_menu_date_func,
    edit_cafe_menu_meal_func,
    edit_cafe_menu_start_func,
    edit_cafe_menu_text_func,
)

router = Router(name=__name__)
router.message.filter(HasCafeMenuRole())
router.callback_query.filter(HasCafeMenuRole())


@router.callback_query(EditMeal.filter(F.meal == Meal.AUTO_ALL))
async def auto_update_cafe_menu_handler(
    callback: "CallbackQuery",
    settings: "Settings",
    repo: "Repository",
) -> None:
    """Обработчик кнопки "Загрузить меню".

    Загружает и обрабатывает PDF расписание еды с сайта лицея.
    """
    text = await process_cafe_menu(repo.menu, settings.other.timeout)
    await callback.message.edit_text(
        text=text,
        reply_markup=await admin_panel_keyboard(repo.user, callback.from_user.id),
    )


@router.callback_query(AdminEditMenu.filter(F.menu == BotMenu.CAFE_MENU))
async def edit_cafe_menu_start_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
) -> None:
    """Обработчик кнопки "Изменить меню"."""
    text = await edit_cafe_menu_start_func(callback.message.message_id, state)
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


@router.callback_query(StateFilter(EditingMenu.choose_meal), EditMeal.filter())
async def edit_cafe_menu_meal_handler(
    callback: "CallbackQuery",
    callback_data: "EditMeal",
    state: "FSMContext",
    repo: "Repository",
) -> None:
    """Обработчик кнопки с выбором приёма пищи для изменения."""
    text = await edit_cafe_menu_meal_func(callback_data.meal, state, repo.menu)
    await callback.message.edit_text(text=text, reply_markup=cancel_state_keyboard)


@router.message(StateFilter(EditingMenu.write))
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


@router.callback_query(
    StateFilter(EditingMenu.write),
    InStateData.filter(F.action == Action.CONFIRM),
)
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
