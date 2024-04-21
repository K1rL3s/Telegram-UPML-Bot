from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.text_decorations import html_decoration as html

from bot.callbacks import UniverData
from bot.keyboards import univers_titles_keyboard
from shared.database.repository import UniverRepository
from shared.utils.phrases import SUCCESS
from shared.utils.states import AddingUniver, DeletingUniver


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
    description = html_text
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


async def delete_univer_func(state: FSMContext, callback_data: UniverData) -> str:
    await state.set_state(DeletingUniver.confirm)
    await state.set_data(
        {
            "id": callback_data.id,
            "city": callback_data.city,
            "page": callback_data.page,
        }
    )

    return f"Вы уверены, что хотите удалить этот ВУЗ (#{callback_data.id})?"


async def delete_univer_confirm_func(
    state: FSMContext,
    univer_repo: UniverRepository,
) -> tuple[str, InlineKeyboardMarkup]:
    data = await state.get_data()
    univer_id: int = data["id"]
    city: str = data["city"]
    page: int = data["page"]

    await state.clear()

    await univer_repo.delete(univer_id)

    return SUCCESS, await univers_titles_keyboard(page, city, univer_repo)
