from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks import OpenMenu
from bot.keyboards import (
    go_to_main_menu_keyboard,
    main_menu_keyboard,
    start_reply_keyboard,
)
from bot.middlewares.inner.save_user import SaveUpdateUserMiddleware
from shared.database.repository.repository import Repository
from shared.utils.enums import BotMenu, SlashCommand, TextCommand

router = Router(name=__name__)
router.message.middleware(SaveUpdateUserMiddleware())

START_TEXT = """
👋 Привет! Я - стартовое меню
/help - Подробнее о том, что я могу

📞 <a href="https://hello.k1rles.ru/">Связь с разработчиком</a> 📱
🐍 <a href="https://github.com/K1rL3s/Telegram-UPML-Bot">Код бота</a> ⭐
""".strip()

MAIN_MENU_TEXT = "🏠 Я - главное меню"

HELP_TEXT = """
🤖 Я - Бот-помощник для учеников Югорского физико-математического лицея-интерната
С моей помощью можно узнать расписание уроков и элективов, еду в столовой и поставить таймер для прачечной

🔵 Для навигации вы можете использовать кнопки на клавиатуре или эти команды:
/start - Стартовое меню, перезапуск бота
/help - Информации обо мне
/menu - Начальная точка навигации
/cafe - Меню в столовой
/lessons - Расписание уроков
/laundry - Таймер для прачечной
/electives - Расписание элективов
/educators - Расписание работы воспитателей
/settings - Ваши настройки: класс, время таймеров и оповещения
/cancel - Отмена ввода, если бот его ждёт
"""  # noqa


@router.message(F.text == TextCommand.START, StateFilter("*"))
@router.message(CommandStart(), StateFilter("*"))
async def start_handler(
    message: "Message",
    repo: "Repository",
    state: "FSMContext",
) -> None:
    """Обработчик команды "/start"."""
    await state.clear()
    await message.reply(
        text=START_TEXT,
        reply_markup=await start_reply_keyboard(repo.user, message.from_user.id),
    )


@router.callback_query(OpenMenu.filter(F.menu == BotMenu.MAIN_MENU))
async def main_menu_callback_handler(
    callback: "CallbackQuery",
    repo: "Repository",
) -> None:
    """Обработчик кнопки "Главное меню"."""
    keyboard = await main_menu_keyboard(repo.user, callback.from_user.id)
    await callback.message.edit_text(text=MAIN_MENU_TEXT, reply_markup=keyboard)


@router.message(F.text == TextCommand.MENU)
@router.message(Command(SlashCommand.MENU))
async def main_menu_message_handler(
    message: "Message",
    repo: "Repository",
) -> None:
    """Обработчик команды "/menu"."""
    keyboard = await main_menu_keyboard(repo.user, message.from_user.id)
    await message.reply(text=MAIN_MENU_TEXT, reply_markup=keyboard)


@router.message(F.text == TextCommand.HELP)
@router.message(Command(SlashCommand.HELP))
async def help_handler(message: "Message") -> None:
    """Обработчик команды "/help"."""
    await message.reply(text=HELP_TEXT, reply_markup=go_to_main_menu_keyboard)
