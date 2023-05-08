from aiogram import Dispatcher, types

from src.handlers.lessons import get_lessons_text_and_image_id
from src.keyboards import lessons_keyboard
from src.utils.consts import CallbackData
from src.utils.dateformat import date_by_format


async def open_date_lessons_view(callback: types.CallbackQuery) -> None:
    lessons_date = date_by_format(
        callback.data.replace(
            CallbackData.OPEN_LESSONS_ON_, ''
        )
    )
    text, images = get_lessons_text_and_image_id(
        callback.from_user.id, lessons_date
    )

    if images[0]:
        await callback.message.answer_photo(
            caption=text,
            photo=images[0],
            reply_markup=lessons_keyboard(lessons_date)
        )
    else:
        method = 'reply' if callback.message.photo else 'edit_text'
        await getattr(callback.message, method)(
            text=text,
            reply_markup=lessons_keyboard(lessons_date)
        )

    # if callback.message.photo:
    #     await callback.message.delete()


def register_lessons_view(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(
        open_date_lessons_view,
        lambda callback: callback.data.startswith(
            CallbackData.OPEN_LESSONS_ON_
        )
    )
