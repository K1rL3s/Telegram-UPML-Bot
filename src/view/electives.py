from aiogram import Router, types
from aiogram.filters import Text

from src.utils.consts import CallbackData


router = Router(name='electives')


@router.callback_query(Text(CallbackData.OPEN_ELECTIVES))
async def electives_view(callback: types.CallbackQuery) -> None:
    await callback.message.edit_text(
        text='🥲',
        reply_markup=callback.message.reply_markup
    )
