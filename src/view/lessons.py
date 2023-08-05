from aiogram import Router, types
from aiogram.filters import Text
from aiogram.methods import SendMediaGroup

from src.handlers.lessons import get_lessons_text_and_image_id
from src.keyboards import lessons_keyboard
from src.utils.consts import CallbackData
from src.utils.datehelp import date_by_format
from src.utils.decorators import save_new_user_decor


router = Router(name='lessons')


@router.callback_query(Text(startswith=CallbackData.OPEN_LESSONS_ON_))
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
        messages = await SendMediaGroup(
            chat_id=callback.message.chat.id,
            media=[
                types.InputMediaPhoto(media=media_id)
                for media_id in images
                if media_id
            ]
        )
        await messages[0].reply(
            text=text,
            reply_markup=lessons_keyboard(lessons_date)
        )
    else:
        await callback.message.edit_text(
            text=text,
            reply_markup=lessons_keyboard(lessons_date)
        )
