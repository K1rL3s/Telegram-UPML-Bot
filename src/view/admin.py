from io import BytesIO

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from src.handlers.admin import load_lessons_handler
from src.keyboards import cancel_state_keyboard, start_menu_keyboard
from src.upml.save_cafe_menu import save_cafe_menu
from src.utils.decorators import admin_required
from src.utils.states import LoadingLessons
from src.utils.throttling import rate_limit


@admin_required
async def update_cafe_menu_view(message: types.Message, *_, **__) -> None:
    text = await save_cafe_menu()

    await message.reply(
        text=text,
        reply_markup=start_menu_keyboard
    )


@admin_required
async def start_load_lessons_view(message: types.Message, *_, **__) -> None:
    await LoadingLessons.image.set()

    await message.reply(
        text='Отправьте изображение(-я) расписания уроков',
        reply_markup=cancel_state_keyboard
    )


@rate_limit(0)
@admin_required
async def load_lessons_view(
        message: types.Message, state: FSMContext, *_, **__
) -> None:
    await message.photo[-1].download(destination_file=(image := BytesIO()))

    text = await load_lessons_handler(message.chat.id, image)

    await message.reply(
        text=text,
        reply_markup=start_menu_keyboard
    )

    await state.finish()


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
