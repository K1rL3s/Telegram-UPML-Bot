from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.filters import StateFilter


from bot.filters import IsAdmin
from bot.funcs.admin.admin import get_educators_schedule_by_date
from bot.keyboards import cancel_state_keyboard, confirm_cancel_keyboard
from bot.keyboards.admin.admin import admin_panel_keyboard
from bot.utils.enums import AdminCallback
from bot.utils.datehelp import date_by_format, date_today, format_date
from bot.utils.phrases import DONT_UNDERSTAND_DATE
from bot.utils.states import EditingEducators

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext
    from aiogram.types import CallbackQuery, Message

    from bot.database.repository.repository import Repository


router = Router(name=__name__)


@router.callback_query(F.data == AdminCallback.EDIT_EDUCATORS, IsAdmin())
async def edit_educators_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
) -> None:
    """Обработчик ввода даты для изменения расписания воспитателей."""
    text = f"""
Введите дату дня, расписание которого хотите изменить в формате <b>ДД.ММ.ГГГГ</b>
Например, <code>{format_date(date_today())}</code>
""".strip()

    await state.set_state(EditingEducators.choose_date)
    await state.update_data(start_id=callback.message.message_id)

    await callback.message.edit_text(text=text, reply_markup=cancel_state_keyboard)


@router.message(StateFilter(EditingEducators.choose_date), IsAdmin())
async def edit_educators_date_handler(
    message: "Message",
    state: "FSMContext",
    repo: "Repository",
) -> None:
    """Обработчик ввода даты для изменения расписания воспитателей."""
    if edit_date := date_by_format(message.text):
        schedule = await get_educators_schedule_by_date(repo.educators, edit_date)
        text = (
            f"<b>Дата</b>: <code>{format_date(edit_date)}</code>\n"
            f"<b>Расписание</b>:\n{schedule}\n\n"
            "Чтобы изменить, отправьте <b>одним сообщением</b> "
            "изменённую версию."
        )
        await state.set_state(EditingEducators.writing)
        await state.update_data(edit_date=edit_date)
    else:
        text = DONT_UNDERSTAND_DATE

    start_id = (await state.get_data())["start_id"]

    await message.bot.edit_message_text(
        text=text,
        chat_id=message.chat.id,
        message_id=start_id,
        reply_markup=cancel_state_keyboard,
    )

    await message.delete()  # ?


@router.message(StateFilter(EditingEducators.writing), IsAdmin())
async def edit_educators_text_handler(
    message: "Message",
    state: "FSMContext",
) -> None:
    """Обработчик сообщения с изменённым расписанием воспитателей."""
    data = await state.get_data()
    start_id = data["start_id"]
    edit_date = data["edit_date"]

    new_text = message.html_text.strip()
    new_ids = data.get("new_ids", []) + [message.message_id]
    await state.update_data(new_text=new_text, new_ids=new_ids)

    text = (
        f"<b>Дата</b>: <code>{format_date(edit_date)}</code>\n"
        f"<b>Расписание</b>:\n{new_text}\n\n"
        "Для сохранения нажмите кнопку. Если хотите изменить, "
        "отправьте сообщение повторно."
    )

    await message.bot.edit_message_text(
        text=text,
        chat_id=message.chat.id,
        message_id=start_id,
        reply_markup=confirm_cancel_keyboard,
    )


@router.callback_query(StateFilter(EditingEducators.writing), IsAdmin())
async def edit_educators_confirm_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
    repo: "Repository",
) -> None:
    """Обработчик подтверждения изменения расписания воспитетелей."""
    data = await state.get_data()
    edit_date = data["edit_date"]
    new_text = data["new_text"]
    new_ids = data["new_ids"]

    await state.clear()

    await repo.educators.save_or_update_to_db(
        edit_date,
        new_text,
        callback.from_user.id,
    )

    text = (
        f"<b>Расписание воспитателей</b> на "
        f"<b>{format_date(edit_date)}</b> успешно изменено!"
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=await admin_panel_keyboard(repo.user, callback.from_user.id),
    )

    for new_id in new_ids:
        await callback.bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=new_id,
        )
