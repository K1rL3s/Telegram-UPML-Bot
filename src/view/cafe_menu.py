from aiogram import Router, types
from aiogram.filters import Text

from src.handlers.cafe_menu import get_formatted_menu_by_date
from src.keyboards import cafe_menu_keyboard
from src.utils.consts import CallbackData
from src.utils.datehelp import date_by_format


router = Router(name='cafe_menu')


@router.callback_query(Text(startswith=CallbackData.OPEN_CAFE_MENU_ON_))
async def open_date_cafe_menu(callback: types.CallbackQuery) -> None:
    """
    Обработчик кнопки "Меню", открывает расписание еды на текущий день.
    """
    menu_date = date_by_format(
        callback.data.replace(
            CallbackData.OPEN_CAFE_MENU_ON_, ''
        )
    )
    text = get_formatted_menu_by_date(menu_date)

    await callback.message.edit_text(
        text=text,
        reply_markup=cafe_menu_keyboard(menu_date)
    )
