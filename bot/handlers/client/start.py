from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.database.repository.repository import Repository
from bot.filters import IsAdmin, SaveUser
from bot.keyboards import main_menu_inline_keyboard, admin_panel_keyboard
from bot.keyboards.client.start import start_reply_keyboard
from bot.utils.consts import (
    AdminCallback,
    UserCallback,
    SlashCommands,
    TextCommands,
)


router = Router(name=__name__)


@router.message(F.text == TextCommands.START, SaveUser())
@router.message(Command(SlashCommands.START), SaveUser())
async def start_handler(message: Message, repo: Repository) -> None:
    """
    Обработчик команды "/start".
    """
    text = "Привет! Я - стартовое меню.\nИспользуй команду /menu"

    await message.reply(
        text=text, reply_markup=await start_reply_keyboard(repo, message.from_user.id)
    )


@router.message(F.text == TextCommands.MENU, SaveUser())
@router.message(Command(SlashCommands.MENU))
@router.callback_query(F.data == UserCallback.OPEN_MAIN_MENU, SaveUser())
async def main_menu_handler(
    message: Message | CallbackQuery,
    repo: Repository,
) -> None:
    """
    Обработчик команды "/menu" и кнопки "Главное меню".
    """
    text = "Привет! Я - главное меню."
    keyboard = await main_menu_inline_keyboard(repo, message.from_user.id)

    if isinstance(message, CallbackQuery):
        await message.message.edit_text(text=text, reply_markup=keyboard)
    else:
        await message.reply(text=text, reply_markup=keyboard)


@router.message(F.text == TextCommands.HELP, SaveUser())
@router.message(Command(SlashCommands.HELP), SaveUser())
async def help_handler(message: Message) -> None:
    """
    Обработчик команды "/help".
    """
    await message.reply("Помощь!")


@router.message(F.text == TextCommands.ADMIN_PANEL, IsAdmin())
@router.callback_query(F.data == AdminCallback.OPEN_ADMIN_PANEL, IsAdmin())
async def admin_panel_handler(
    callback: CallbackQuery | Message,
    repo: Repository,
) -> None:
    """
    Обработчик кнопки "Админ панель".
    """
    text = """
Привет! Я - админ панель.

*Загрузить меню* - автоматическое обновление еды информацией с сайта лицея.
*Изменить меню* - ручное изменение еды.
*Загрузить уроки* - ручная загрузка изображений с расписанием уроков.
*Уведомление* - сделать оповещение.
""".strip()
    keyboard = await admin_panel_keyboard(repo, callback.from_user.id)

    if isinstance(callback, CallbackQuery):
        await callback.message.edit_text(text=text, reply_markup=keyboard)
    else:
        await callback.answer(text=text, reply_markup=keyboard)


@router.message(F.text == TextCommands.CANCEL, StateFilter("*"))
@router.message(Command(SlashCommands.CANCEL, SlashCommands.STOP), StateFilter("*"))
@router.callback_query(F.data == UserCallback.CANCEL_STATE, StateFilter("*"))
async def cancel_state(
    message: Message | CallbackQuery,
    state: FSMContext,
    repo: Repository,
) -> None:
    """
    Обработчик кнопок с отменой состояний и команд "/cancel", "/stop".
    """
    if state.get_state() is None:
        return

    await state.clear()
    await main_menu_handler(message, repo)
