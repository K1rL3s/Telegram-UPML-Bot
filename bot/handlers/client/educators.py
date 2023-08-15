from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery

from bot.database.db_funcs import Repository
from bot.funcs.educators import get_formatted_educators_schedule_by_date
from bot.keyboards import educators_keyboard
from bot.utils.consts import CallbackData, SlashCommands, TextCommands
from bot.utils.datehelp import date_by_format


router = Router(name=__name__)


@router.message(F.text == TextCommands.EDUCATORS)
@router.message(Command(SlashCommands.EDUCATORS))
@router.callback_query(F.data.startswith(CallbackData.OPEN_EDUCATORS_ON_))
async def educators_handler(
        callback: CallbackQuery,
        repo: Repository,
) -> None:
    """
    Обработчик команды "/educators" и кнопки "Воспитатели",
    открывает расписание воспитателей на текущий день.
    """
    if isinstance(callback, CallbackQuery):
        _date = callback.data.replace(CallbackData.OPEN_EDUCATORS_ON_, '')
    else:
        _date = 'today'
    schedule_date = date_by_format(_date)

    text = await get_formatted_educators_schedule_by_date(repo, schedule_date)

    if isinstance(callback, CallbackQuery):
        await callback.message.edit_text(
            text=text,
            reply_markup=educators_keyboard(schedule_date),
            parse_mode='html'
        )
    else:
        await callback.answer(
            text=text,
            reply_markup=educators_keyboard(schedule_date),
            parse_mode='html'
        )
