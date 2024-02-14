from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks import AdminEditMenu, InStateData, UniverData
from bot.filters import HasUniversRole
from bot.keyboards import (
    admin_panel_keyboard,
    cancel_state_keyboard,
    confirm_cancel_keyboard,
)
from shared.database.repository.repository import Repository
from shared.utils.enums import Action, BotMenu
from shared.utils.states import AddingUniver, DeletingUniver

from .funcs import (
    add_univer_city_func,
    add_univer_confirm_func,
    add_univer_description_func,
    add_univer_func,
    add_univer_title_func,
    delete_univer_confirm_func,
    delete_univer_func,
)

router = Router()

router.message.filter(HasUniversRole())
router.callback_query.filter(HasUniversRole())


@router.callback_query(AdminEditMenu.filter(F.menu == BotMenu.UNIVERS))
async def add_univer_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """Обработчик кнопки "Добавить ВУЗ"."""
    text = await add_univer_func(callback.message.message_id, state)
    await callback.message.edit_text(text=text, reply_markup=cancel_state_keyboard)


@router.message(AddingUniver.title, F.text)
async def add_univer_title_handler(
    message: Message,
    bot: Bot,
    state: FSMContext,
) -> None:
    """Обработчик ввода названия вуза."""
    text, start_id = await add_univer_title_func(message.text, state)
    await bot.edit_message_text(
        text=text,
        chat_id=message.chat.id,
        message_id=start_id,
        reply_markup=cancel_state_keyboard,
    )
    await message.delete()


@router.message(AddingUniver.city, F.text)
async def add_univer_city_handler(
    message: Message,
    bot: Bot,
    state: FSMContext,
) -> None:
    """Обработчик ввода города вуза."""
    text, start_id = await add_univer_city_func(message.text, state)
    await bot.edit_message_text(
        text=text,
        chat_id=message.chat.id,
        message_id=start_id,
        reply_markup=cancel_state_keyboard,
    )
    await message.delete()


@router.message(AddingUniver.description, F.text)
async def add_univer_description_handler(
    message: Message,
    bot: Bot,
    state: FSMContext,
) -> None:
    """Обработчик ввода описания вуза."""
    text, start_id = await add_univer_description_func(message.html_text, state)
    await bot.edit_message_text(
        text=text,
        chat_id=message.chat.id,
        message_id=start_id,
        reply_markup=confirm_cancel_keyboard,
    )
    await message.delete()


@router.callback_query(
    AddingUniver.confirm,
    InStateData.filter(F.action == Action.CONFIRM),
)
async def add_univer_confirm_handler(
    callback: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    repo: Repository,
) -> None:
    """Обработчик подтверждения сохранения вуза."""
    text, start_id = await add_univer_confirm_func(state, repo.univers)
    chat_id = callback.message.chat.id
    await bot.edit_message_text(
        text=text,
        chat_id=chat_id,
        message_id=start_id,
        reply_markup=await admin_panel_keyboard(repo.user, chat_id),
    )


@router.callback_query(
    UniverData.filter(F.action == Action.DELETE),
    UniverData.filter(F.id.is_not(None)),
)
async def delete_univer_handler(
    callback: CallbackQuery,
    callback_data: UniverData,
    state: FSMContext,
) -> None:
    text = await delete_univer_func(state, callback_data)
    await callback.message.edit_text(text=text, reply_markup=confirm_cancel_keyboard)


@router.callback_query(
    DeletingUniver.confirm,
    InStateData.filter(F.action == Action.CONFIRM),
)
async def delete_univer_confirm_handler(
    callback: CallbackQuery,
    state: FSMContext,
    repo: Repository,
) -> None:
    text, keyboard = await delete_univer_confirm_func(state, repo.univers)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
