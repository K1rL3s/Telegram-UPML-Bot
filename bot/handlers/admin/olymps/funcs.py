from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.text_decorations import html_decoration as html

from bot.callbacks import OlympData
from bot.keyboards import olymps_titles_keyboard
from shared.database.repository import OlympRepository
from shared.utils.phrases import SUCCESS
from shared.utils.states import AddingOlymp, DeletingOlymp


async def add_olymp_func(
    message_id: int,
    state: "FSMContext",
) -> str:
    await state.set_state(AddingOlymp.title)
    await state.update_data(start_id=message_id)

    return "Как называется олимпиада? До 64 символов."


async def add_olymp_title_func(
    text: str,
    state: "FSMContext",
) -> tuple[str, int]:
    title = html.quote(text)
    await state.set_state(AddingOlymp.subject)
    data = await state.update_data(title=title)
    start_id: int = data["start_id"]

    text = (
        f"<b>Название</b>: <code>{title}</code>\n\n"
        "По какому предмету эта олимпиада? Чувствительно к регистру!"
    )

    return text, start_id


async def add_olymp_subject_func(
    text: str,
    state: "FSMContext",
) -> tuple[str, int]:
    subject = html.quote(text)
    await state.set_state(AddingOlymp.description)
    data = await state.update_data(subject=subject)
    start_id: int = data["start_id"]
    title: str = data["title"]

    text = (
        f"<b>Название</b>: <code>{title}</code>\n"
        f"<b>Предмет</b>: <code>{subject}</code>\n\n"
        "Расскажите про олимпиаду. До 3584 (512x7) символов."
    )

    return text, start_id


async def add_olymp_description_func(
    html_text: str,
    state: "FSMContext",
) -> tuple[str, int]:
    description = html_text
    await state.set_state(AddingOlymp.confirm)
    data = await state.update_data(description=description)
    start_id: int = data["start_id"]
    subject: str = data["subject"]
    title: str = data["title"]

    text = (
        f"<b>Название</b>: <code>{title}</code>\n"
        f"<b>Предмет</b>: <code>{subject}</code>\n"
        f"<b>Описание</b>:\n{description}\n\n"
        "<b>Сохраняем?</b>"
    )

    return text, start_id


async def add_olymp_confirm_func(
    state: "FSMContext",
    repo: OlympRepository,
) -> tuple[str, int]:
    data = await state.get_data()
    start_id: int = data["start_id"]
    subject: str = data["subject"]
    title: str = data["title"]
    description: str = data["description"]

    await state.clear()

    await repo.add(title, subject, description)

    text = (
        f"Олимпиада <code>{title}</code> по <code>{subject}</code> успешно добавлена!"
    )
    return text, start_id


async def delete_olymp_func(state: FSMContext, callback_data: OlympData) -> str:
    await state.set_state(DeletingOlymp.confirm)
    await state.set_data(
        {
            "id": callback_data.id,
            "subject": callback_data.subject,
            "page": callback_data.page,
        }
    )

    return f"Вы уверены, что хотите удалить эту олимпиаду (#{callback_data.id})?"


async def delete_olymp_confirm_func(
    state: FSMContext,
    olymp_repo: OlympRepository,
) -> tuple[str, InlineKeyboardMarkup]:
    data = await state.get_data()
    olymp_id: int = data["id"]
    subject: str = data["subject"]
    page: int = data["page"]

    await state.clear()

    await olymp_repo.delete(olymp_id)

    return SUCCESS, await olymps_titles_keyboard(page, subject, olymp_repo)
