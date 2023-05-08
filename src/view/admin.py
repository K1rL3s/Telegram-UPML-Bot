from io import BytesIO

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from src.handlers.admin import first_load_lessons_handler
from src.keyboards import start_menu_keyboard
from src.upml.save_cafe_menu import save_cafe_menu
from src.utils.states import LoadingLessons
from src.utils.throttling import rate_limit


async def update_cafe_menu_view(message: types.Message) -> None:
    text = str(await save_cafe_menu())

    await message.reply(
        text=text,
        reply_markup=start_menu_keyboard
    )


async def start_load_lessons_view(message: types.Message) -> None:
    await LoadingLessons.image.set()

    await message.reply(
        text='Отправьте изображение(-я) расписаний уроков',
        reply_markup=start_menu_keyboard
    )


@rate_limit(0)
async def load_lessons_view(message: types.Message, state: FSMContext) -> None:
    await message.photo[-1].download(destination_file=(image := BytesIO()))

    text = await first_load_lessons_handler(message.chat.id, image)

    await message.reply(
        text=text
    )


def register_admin_view(dp: Dispatcher):
    dp.register_message_handler(
        update_cafe_menu_view,
        commands=['update']
    )
    dp.register_message_handler(
        start_load_lessons_view,
        commands=['load']
    )
    dp.register_message_handler(
        load_lessons_view,
        content_types=['photo'],
        state=LoadingLessons.image
    )

