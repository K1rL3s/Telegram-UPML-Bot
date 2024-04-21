from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot.callbacks import OpenMenu
from bot.keyboards import admin_panel_keyboard
from shared.database.repository.repository import Repository
from shared.utils.enums import BotMenu, TextCommand

router = Router(name=__name__)

ADMIN_START_TEXT = """
❗Я - админ панель. Вот мои команды:
<b>Загрузить меню</b> - автоматическое обновление еды информацией с сайта лицея
<b>Изменить меню</b> - ручное изменение еды
<b>Загрузить уроки</b> - ручная загрузка изображений с расписанием уроков
<b>Уведомление</b> - сделать оповещение
<b>Добавить ВУЗ</b> - добавить университет в раздел "поступающим"
<b>Добавить олимпиаду</b> - добавить олимпиаду в раздел "поступающим"
<b>Изменить расписание воспитателей</b> - ручное изменение расписания воспитателей
""".strip()


@router.callback_query(OpenMenu.filter(F.menu == BotMenu.ADMIN_PANEL))
async def admin_panel_callback_handler(
    callback: "CallbackQuery",
    repo: "Repository",
) -> None:
    """Обработчик кнопки "Админ панель"."""
    keyboard = await admin_panel_keyboard(repo.user, callback.from_user.id)
    await callback.message.edit_text(text=ADMIN_START_TEXT, reply_markup=keyboard)


@router.message(F.text == TextCommand.ADMIN_PANEL)
async def admin_panel_message_handler(
    message: "Message",
    repo: "Repository",
) -> None:
    """Обработчик команды "Админ панель"."""
    keyboard = await admin_panel_keyboard(repo.user, message.from_user.id)
    await message.answer(text=ADMIN_START_TEXT, reply_markup=keyboard)
