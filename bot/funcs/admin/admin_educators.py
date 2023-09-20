from typing import TYPE_CHECKING

from bot.funcs.admin.admin import get_educators_schedule_by_date
from bot.utils.datehelp import date_by_format, format_date
from bot.utils.phrases import DONT_UNDERSTAND_DATE
from bot.utils.states import EditingEducators

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext

    from bot.database.repository import EducatorsScheduleRepository


async def edit_educators_date_func(
    text: str,
    state: "FSMContext",
    repo: "EducatorsScheduleRepository",
) -> tuple[str, int]:
    """
    Обработчик ввода даты для изменения расписания воспитателей.

    :param text: Сообщение пользователя.
    :param state: Состояние пользователя.
    :param repo: Репозиторий расписаний воспитателей.
    :return: Сообщение пользователю и айди начального сообщения бота.
    """
    if edit_date := date_by_format(text):
        schedule = await get_educators_schedule_by_date(repo, edit_date)
        text = (
            f"<b>Дата</b>: <code>{format_date(edit_date)}</code>\n"
            f"<b>Расписание</b>:\n{schedule}\n\n"
            "Чтобы изменить, отправьте <b>одним сообщением</b> "
            "изменённую версию."
        )
        await state.set_state(EditingEducators.writing)
        await state.update_data(edit_date=format_date(edit_date))
    else:
        text = DONT_UNDERSTAND_DATE

    return text, (await state.get_data())["start_id"]


async def edit_educators_text_func(
    html_text: str,
    message_id: int,
    state: "FSMContext",
) -> tuple[str, int]:
    """
    Обработчик сообщения с изменённым расписанием воспитателей.

    :param html_text: Сообщение пользователя в html'е.
    :param message_id: Айди сообщения пользователя.
    :param state: Состояние пользователя.
    :return: Сообщение пользователю и айди начального сообщения бота.
    """
    data = await state.get_data()
    start_id = data["start_id"]
    edit_date = date_by_format(data["edit_date"])

    new_text = html_text.strip()
    new_ids = data.get("new_ids", []) + [message_id]
    await state.update_data(new_text=new_text, new_ids=new_ids)

    text = (
        f"<b>Дата</b>: <code>{format_date(edit_date)}</code>\n"
        f"<b>Расписание</b>:\n{new_text}\n\n"
        "Для сохранения нажмите кнопку. Если хотите изменить, "
        "отправьте сообщение повторно."
    )

    return text, start_id


async def edit_educators_confirm_func(
    user_id: int,
    state: "FSMContext",
    repo: "EducatorsScheduleRepository",
) -> tuple[str, list[int]]:
    """
    Обработчик подтверждения изменения расписания воспитетелей.

    :param user_id: ТГ Айди.
    :param state: Состояние пользователя.
    :param repo: Репозиторий расписаний воспитателей.
    :return: Сообщение пользователю и айдишники его сообщений с изменениями.
    """
    data = await state.get_data()
    new_text = data["new_text"]
    new_ids = data["new_ids"]
    edit_date = date_by_format(data["edit_date"])

    await state.clear()

    await repo.save_or_update_to_db(edit_date, new_text, user_id)

    text = (
        f"<b>Расписание воспитателей</b> на "
        f"<b>{format_date(edit_date)}</b> успешно изменено!"
    )

    return text, new_ids
