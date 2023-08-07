from aiogram import F, Router, types
from aiogram.filters import Command

from src.keyboards import main_menu_keyboard
from src.utils.consts import CallbackData, Commands


router = Router(name='electives')


@router.message(Command(Commands.ELECTIVES))
@router.callback_query(F.data == CallbackData.OPEN_ELECTIVES)
async def electives_view(
        callback: types.CallbackQuery | types.Message
) -> None:
    ...

    if isinstance(callback, types.CallbackQuery):
        await callback.message.edit_text(
            text='🥲',
            reply_markup=callback.message.reply_markup
        )
    else:
        await callback.answer(
            text='🥲',
            reply_markup=await main_menu_keyboard(callback.from_user.id)
        )
