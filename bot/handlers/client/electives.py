from aiogram import F, Router, types
from aiogram.filters import Command

from bot.database.db_funcs import Repository
from bot.keyboards import main_menu_keyboard
from bot.utils.consts import CallbackData, Commands


router = Router(name=__name__)


@router.message(Command(Commands.ELECTIVES))
@router.callback_query(F.data == CallbackData.OPEN_ELECTIVES)
async def electives_handler(
        callback: types.CallbackQuery | types.Message,
        repo: Repository,
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
            reply_markup=await main_menu_keyboard(repo, callback.from_user.id)
        )
