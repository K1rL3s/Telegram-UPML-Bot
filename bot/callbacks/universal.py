from aiogram.filters.callback_data import CallbackData


class OpenMenu(CallbackData, prefix="open_menu"):
    """Фабрика для открытия разных меню бота."""

    menu: str
    date: str | None = None


class InStateData(CallbackData, prefix="in_state"):
    """Фабрика для подтверждения и отмены в состояниях."""

    action: str
