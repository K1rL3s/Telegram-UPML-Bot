from typing import TYPE_CHECKING

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InputMediaPhoto, Message

from bot.filters import SaveUpdateUser
from bot.funcs.lessons import get_lessons_for_user
from bot.keyboards import lessons_keyboard
from bot.utils.enums import SlashCommands, TextCommands, UserCallback
from bot.utils.datehelp import date_by_format

if TYPE_CHECKING:
    import datetime as dt

    from bot.database.repository.repository import Repository


router = Router(name=__name__)


async def send_lessons_images(
    user_id: int,
    chat_id: int,
    date: "dt.date",
    bot: "Bot",
    repo: "Repository",
) -> str | None:
    """
    Общий код обработчиков просмотра уроков. Если имеется, отправляет фото расписания.

    Отправляет расписание уроков паралелли и класса, если выбран класс.
    Отправляет расписание двух паралеллей, если не выбран класс.

    :param user_id: ТГ Айди.
    :param chat_id: Айди чата с пользователем.
    :param date: Дата уроков.
    :param bot: ТГ Бот.
    :param repo: Доступ к базе данных.
    :return: Сообщение для пользователя.
    """
    text, images = await get_lessons_for_user(
        repo.settings,
        repo.lessons,
        user_id,
        date,
    )

    if any(images):
        messages = await bot.send_media_group(
            chat_id=chat_id,
            media=[InputMediaPhoto(media=media_id) for media_id in images if media_id],
        )
        await messages[0].reply(text=text, reply_markup=lessons_keyboard(date))
        return

    return text


@router.callback_query(
    F.data.startswith(UserCallback.OPEN_LESSONS_ON_),
    SaveUpdateUser(),
)
async def date_lessons_callback_handler(
    callback: "CallbackQuery",
    repo: "Repository",
) -> None:
    """Обработчик кнопки "Уроки"."""
    date_ = callback.data.replace(UserCallback.OPEN_LESSONS_ON_, "")
    lessons_date = date_by_format(date_)

    text = await send_lessons_images(
        callback.from_user.id,
        callback.message.chat.id,
        lessons_date,
        callback.bot,
        repo,
    )

    if text:
        await callback.message.edit_text(
            text=text,
            reply_markup=lessons_keyboard(lessons_date),
        )


@router.message(F.text == TextCommands.LESSONS, SaveUpdateUser())
@router.message(Command(SlashCommands.LESSONS), SaveUpdateUser())
async def date_lessons_message_handler(
    message: "Message",
    repo: "Repository",
) -> None:
    """Обработчик команды "Уроки"."""
    date_ = "today"
    lessons_date = date_by_format(date_)

    text = await send_lessons_images(
        message.from_user.id,
        message.chat.id,
        lessons_date,
        message.bot,
        repo,
    )

    if text:
        await message.answer(text=text, reply_markup=lessons_keyboard(lessons_date))
