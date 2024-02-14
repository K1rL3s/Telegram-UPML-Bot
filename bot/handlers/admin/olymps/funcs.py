from aiogram.fsm.context import FSMContext
from aiogram.utils.text_decorations import html_decoration as html

from shared.database.repository import OlympRepository
from shared.utils.states import AddingOlymp


async def add_olymp_func(
    message_id: int,
    state: "FSMContext",
) -> str:
    """
    Обработчик кнопки "Добавить олимпиаду".

    :param message_id: Начальное сообщение бота.
    :param state: Состояние пользователя.
    :return: Сообщение для пользователя.
    """
    await state.set_state(AddingOlymp.title)
    await state.update_data(start_id=message_id)

    return "Как называется олимпиада? До 64 символов."


async def add_olymp_title_func(
    text: str,
    state: "FSMContext",
) -> tuple[str, int]:
    """
    Обработчик сообщения с названием олимпиады.

    :param text: Сообщение пользователя.
    :param state: Состояние пользователя.
    :return: Сообщение пользователю и айди начального сообщения бота.
    """
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
    """
    Обработчик сообщения с предметом олимпиады.

    :param text: Сообщение пользователя.
    :param state: Состояние пользователя.
    :return: Сообщение пользователю и айди начального сообщения бота.
    """
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
    """
    Обработчик сообщения с описанием олимпиады.

    :param html_text: Сообщение пользователя в html'е.
    :param state: Состояние пользователя.
    :return: Сообщение пользователю и айди начального сообщения бота.
    """
    description = html_text.strip()
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
    """
    Обработчик подтверждения добавления олимпиады.

    :param state: Состояние пользователя.
    :param repo: Репозиторий расписаний воспитателей.
    :return: Сообщение пользователю.
    """
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
