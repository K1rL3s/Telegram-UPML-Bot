from aiogram.fsm.context import FSMContext
from aiogram.utils.text_decorations import html_decoration as html

from shared.database.repository import UniverRepository
from shared.utils.states import AddingUniver


async def add_univer_func(
    message_id: int,
    state: "FSMContext",
) -> str:
    """
    Обработчик кнопки "Добавить вуз".

    :param message_id: Начальное сообщение бота.
    :param state: Состояние пользователя.
    :return: Сообщение для пользователя.
    """
    await state.set_state(AddingUniver.title)
    await state.update_data(start_id=message_id)

    return "Как называется ВУЗ? До 64 символов."


async def add_univer_title_func(
    text: str,
    state: "FSMContext",
) -> tuple[str, int]:
    """
    Обработчик сообщения с названием вуза.

    :param text: Сообщение пользователя.
    :param state: Состояние пользователя.
    :return: Сообщение пользователю и айди начального сообщения бота.
    """
    title = html.quote(text)
    await state.set_state(AddingUniver.city)
    data = await state.update_data(title=title)
    start_id: int = data["start_id"]

    text = (
        f"<b>Название</b>: <code>{title}</code>\n\n"
        "В каком городе этот ВУЗ? Чувствительно к регистру!"
    )

    return text, start_id


async def add_univer_city_func(
    text: str,
    state: "FSMContext",
) -> tuple[str, int]:
    """
    Обработчик сообщения с городом вуза.

    :param text: Сообщение пользователя.
    :param state: Состояние пользователя.
    :return: Сообщение пользователю и айди начального сообщения бота.
    """
    city = html.quote(text)
    await state.set_state(AddingUniver.description)
    data = await state.update_data(city=city)
    start_id: int = data["start_id"]
    title: str = data["title"]

    text = (
        f"<b>Название</b>: <code>{title}</code>\n"
        f"<b>Город</b>: <code>{city}</code>\n\n"
        "Расскажите про ВУЗ. До 3584 (512x7) символов."
    )

    return text, start_id


async def add_univer_description_func(
    html_text: str,
    state: "FSMContext",
) -> tuple[str, int]:
    """
    Обработчик сообщения с описанием вуза.

    :param html_text: Сообщение пользователя в html'е.
    :param state: Состояние пользователя.
    :return: Сообщение пользователю и айди начального сообщения бота.
    """
    description = html_text.strip()
    await state.set_state(AddingUniver.confirm)
    data = await state.update_data(description=description)
    start_id: int = data["start_id"]
    city: str = data["city"]
    title: str = data["title"]

    text = (
        f"<b>Название</b>: <code>{title}</code>\n"
        f"<b>Город</b>: <code>{city}</code>\n"
        f"<b>Описание</b>:\n{description}\n\n"
        "<b>Сохраняем?</b>"
    )

    return text, start_id


async def add_univer_confirm_func(
    state: "FSMContext",
    repo: UniverRepository,
) -> tuple[str, int]:
    """
    Обработчик подтверждения добавления вуза.

    :param state: Состояние пользователя.
    :param repo: Репозиторий расписаний воспитателей.
    :return: Сообщение пользователю.
    """
    data = await state.get_data()
    start_id: int = data["start_id"]
    city: str = data["city"]
    title: str = data["title"]
    description: str = data["description"]

    await state.clear()

    await repo.add(title, city, description)

    text = f"ВУЗ <code>{title}</code> из <code>{city}</code> успешно добавлен!"
    return text, start_id
