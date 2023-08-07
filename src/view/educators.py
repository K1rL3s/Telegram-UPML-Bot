from aiogram import F, Router, types
from aiogram.filters import Command

from src.keyboards import main_menu_keyboard
from src.utils.consts import CallbackData, Commands


router = Router(name='educators')


@router.message(Command(Commands.EDUCATORS))
@router.callback_query(F.data == CallbackData.OPEN_EDUCATORS)
async def educators_view(callback: types.CallbackQuery) -> None:
    ...

    if isinstance(callback, types.CallbackQuery):
        await callback.message.edit_text(
            text='😅',
            reply_markup=callback.message.reply_markup
        )
    else:
        await callback.answer(
            text='😅',
            reply_markup=await main_menu_keyboard(callback.from_user.id)
        )
