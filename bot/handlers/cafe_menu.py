from aiogram import F, Router, types
from aiogram.filters import Command

from bot.database.db_funcs import Repository
from bot.funcs.cafe_menu import get_formatted_menu_by_date
from bot.keyboards import cafe_menu_keyboard
from bot.utils.consts import CallbackData, Commands
from bot.utils.datehelp import date_by_format


router = Router(name=__name__)


@router.message(Command(Commands.CAFE))
@router.callback_query(F.data.startswith(CallbackData.OPEN_CAFE_MENU_ON_))
async def open_date_cafe_menu(
        callback: types.CallbackQuery | types.Message,
        repo: Repository,
) -> None:
    """
    Обработчик команды "/cafe" и кнопки "Меню",
    открывает расписание еды на текущий день.
    """
    if isinstance(callback, types.CallbackQuery):
        _date = callback.data.replace(CallbackData.OPEN_CAFE_MENU_ON_, '')
    else:
        _date = 'today'
    menu_date = date_by_format(_date)

    text = await get_formatted_menu_by_date(repo, menu_date)

    if isinstance(callback, types.CallbackQuery):
        await callback.message.edit_text(
            text=text,
            reply_markup=cafe_menu_keyboard(menu_date)
        )
    else:
        await callback.answer(
            text=text,
            reply_markup=cafe_menu_keyboard(menu_date)
        )
