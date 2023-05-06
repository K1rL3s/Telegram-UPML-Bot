from aiogram import Dispatcher, types


async def start_view(message: types.Message) -> None:
    text = """Привет! Я - стартовое меню."""

    await message.reply(
        text=text,
    )


def register_start_view(dp: Dispatcher):
    dp.register_message_handler(
        start_view,
        commands=['start'],
    )
