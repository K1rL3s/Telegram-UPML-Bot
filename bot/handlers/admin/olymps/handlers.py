from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks import AdminEditMenu, InStateData, OlympData
from bot.filters import HasOlympsRole
from bot.keyboards import (
    admin_panel_keyboard,
    cancel_state_keyboard,
    confirm_cancel_keyboard,
)
from shared.database.repository.repository import Repository
from shared.utils.enums import Action, BotMenu
from shared.utils.states import AddingOlymp, DeletingOlymp

from .funcs import (
    add_olymp_confirm_func,
    add_olymp_description_func,
    add_olymp_func,
    add_olymp_subject_func,
    add_olymp_title_func,
    delete_olymp_confirm_func,
    delete_olymp_func,
)

router = Router()

router.message.filter(HasOlympsRole())
router.callback_query.filter(HasOlympsRole())


@router.callback_query(AdminEditMenu.filter(F.menu == BotMenu.OLYMPS))
async def add_olymp_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """Обработчик кнопки "Добавить олимпиаду"."""
    text = await add_olymp_func(callback.message.message_id, state)
    await callback.message.edit_text(text=text, reply_markup=cancel_state_keyboard)


@router.message(AddingOlymp.title, F.text)
async def add_olymp_title_handler(
    message: Message,
    bot: Bot,
    state: FSMContext,
) -> None:
    """Обработчик ввода названия олимпиады."""
    text, start_id = await add_olymp_title_func(message.text, state)
    await bot.edit_message_text(
        text=text,
        chat_id=message.chat.id,
        message_id=start_id,
        reply_markup=cancel_state_keyboard,
    )
    await message.delete()


@router.message(AddingOlymp.subject, F.text)
async def add_olymp_subject_handler(
    message: Message,
    bot: Bot,
    state: FSMContext,
) -> None:
    """Обработчик ввода предмета олимпиады."""
    text, start_id = await add_olymp_subject_func(message.text, state)
    await bot.edit_message_text(
        text=text,
        chat_id=message.chat.id,
        message_id=start_id,
        reply_markup=cancel_state_keyboard,
    )
    await message.delete()


@router.message(AddingOlymp.description, F.text)
async def add_olymp_description_handler(
    message: Message,
    bot: Bot,
    state: FSMContext,
) -> None:
    """Обработчик ввода описания олимпиады."""
    text, start_id = await add_olymp_description_func(message.html_text, state)
    await bot.edit_message_text(
        text=text,
        chat_id=message.chat.id,
        message_id=start_id,
        reply_markup=confirm_cancel_keyboard,
    )
    await message.delete()


@router.callback_query(
    AddingOlymp.confirm,
    InStateData.filter(F.action == Action.CONFIRM),
)
async def add_olymp_confirm_handler(
    callback: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    repo: Repository,
) -> None:
    """Обработчик подтверждения сохранения олимпиады."""
    text, start_id = await add_olymp_confirm_func(state, repo.olymps)
    chat_id = callback.message.chat.id
    await bot.edit_message_text(
        text=text,
        chat_id=chat_id,
        message_id=start_id,
        reply_markup=await admin_panel_keyboard(repo.user, chat_id),
    )


@router.callback_query(
    OlympData.filter(F.action == Action.DELETE),
    OlympData.filter(F.id.is_not(None)),
)
async def delete_olymp_handler(
    callback: CallbackQuery,
    callback_data: OlympData,
    state: FSMContext,
) -> None:
    text = await delete_olymp_func(state, callback_data)
    await callback.message.edit_text(text=text, reply_markup=confirm_cancel_keyboard)


@router.callback_query(
    DeletingOlymp.confirm,
    InStateData.filter(F.action == Action.CONFIRM),
)
async def delete_olymp_confirm_handler(
    callback: CallbackQuery,
    state: FSMContext,
    repo: Repository,
) -> None:
    text, keyboard = await delete_olymp_confirm_func(state, repo.olymps)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
