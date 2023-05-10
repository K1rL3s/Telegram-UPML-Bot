from io import BytesIO

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from src.handlers.admin import load_lessons_handler
from src.keyboards import cancel_state_keyboard, start_menu_keyboard
from src.keyboards.admin import admin_menu_keyboard
from src.upml.save_cafe_menu import save_cafe_menu
from src.utils.consts import CallbackData
from src.utils.decorators import admin_required
from src.utils.states import LoadingLessons
from src.utils.throttling import rate_limit


@admin_required
async def update_cafe_menu_view(
        callback: types.CallbackQuery, *_, **__
) -> None:
    text = await save_cafe_menu()

    await callback.message.edit_text(
        text=text,
        reply_markup=admin_menu_keyboard(callback.from_user.id)
    )


@admin_required
async def start_load_lessons_view(
        callback: types.CallbackQuery, *_, **__
) -> None:
    await LoadingLessons.image.set()
    text = 'Отправьте изображение(-я) расписания уроков'

    await callback.message.edit_text(
        text=text,
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


def register_admin_updates_view(dp: Dispatcher):
    dp.register_callback_query_handler(
        update_cafe_menu_view,
        text=CallbackData.AUTO_UPDATE_CAFE_MENU
    )
    dp.register_callback_query_handler(
        start_load_lessons_view,
        text=CallbackData.UPLOAD_LESSONS
    )
    dp.register_message_handler(
        load_lessons_view,
        content_types=['photo'],
        state=LoadingLessons.image
    )
