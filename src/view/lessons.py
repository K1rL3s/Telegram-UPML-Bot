from aiogram import Dispatcher, types

from src.handlers.lessons import get_lessons_text_and_image_id
from src.keyboards import lessons_keyboard
from src.utils.consts import CallbackData
from src.utils.datehelp import date_by_format
from src.utils.decorators import save_new_user_decor


@save_new_user_decor
async def open_date_lessons_view(callback: types.CallbackQuery) -> None:
    """
    Обработчик кнопки "Уроки".
    Отправляет расписание уроков паралелли и класса, если выбран класс.
    Отправляет расписание двух паралеллей, если не выбран класс.
    """
    lessons_date = date_by_format(
        callback.data.replace(
            CallbackData.OPEN_LESSONS_ON_, ''
        )
    )
    text, images = get_lessons_text_and_image_id(
        callback.from_user.id, lessons_date
    )

    if images:
        temp = await callback.bot.send_media_group(
            chat_id=callback.message.chat.id,
            media=[
                types.InputMediaPhoto(media_id)
                for media_id in images
                if media_id
            ]
        )
        await temp[0].reply(
            text=text,
            reply_markup=lessons_keyboard(lessons_date)
        )
    else:
        await callback.message.edit_text(
            text=text,
            reply_markup=lessons_keyboard(lessons_date)
        )


def register_lessons_view(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(
        open_date_lessons_view,
        lambda callback: callback.data.startswith(
            CallbackData.OPEN_LESSONS_ON_
        )
    )
