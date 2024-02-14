import datetime as dt

from aiogram.fsm.context import FSMContext

from shared.database.repository import EducatorsScheduleRepository
from shared.utils.datehelp import date_by_format, date_today, format_date
from shared.utils.phrases import DONT_UNDERSTAND_DATE, NO_DATA
from shared.utils.states import EditingEducators


async def edit_educators_start_func(
    message_id: int,
    state: "FSMContext",
) -> str:
    """
    Обработчик кнопки "Изменить расписание воспитателей".

    :param message_id: Начальное сообщение бота.
    :param state: Состояние пользователя.
    :return: Сообщение и клавиатура для пользователя.
    """
    await state.set_state(EditingEducators.choose_date)
    await state.update_data(start_id=message_id)

    return f"""
Введите дату дня, расписание которого хотите изменить в формате <b>ДД.ММ.ГГГГ</b>
Например, <code>{format_date(date_today())}</code>
""".strip()


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
        schedule = getattr(await repo.get(edit_date), "schedule", None) or NO_DATA
        text = (
            f"<b>Дата</b>: <code>{format_date(edit_date)}</code>\n"
            f"<b>Расписание</b>:\n{schedule}\n\n"
            "Чтобы изменить, отправьте <b>одним сообщением</b> "
            "изменённую версию."
        )
        await state.set_state(EditingEducators.write)
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
    start_id: int = data["start_id"]
    edit_date: "dt.date" = date_by_format(data["edit_date"])

    new_text = html_text
    new_ids: list[int] = data.get("new_ids", []) + [message_id]
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
    new_text: str = data["new_text"]
    new_ids: list[int] = data["new_ids"]
    edit_date: "dt.date" = date_by_format(data["edit_date"])

    await state.clear()

    await repo.save_or_update_to_db(edit_date, new_text, user_id)

    text = (
        f"<b>Расписание воспитателей</b> на "
        f"<b>{format_date(edit_date)}</b> успешно изменено!"
    )

    return text, new_ids
