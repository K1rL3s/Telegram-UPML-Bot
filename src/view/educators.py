from aiogram import F, Router, types

from src.utils.consts import CallbackData


router = Router(name='educators')


@router.callback_query(F.data == CallbackData.OPEN_EDUCATORS)
async def educators_view(callback: types.CallbackQuery) -> None:
    await callback.message.edit_text(
        text='😅',
        reply_markup=callback.message.reply_markup
    )
