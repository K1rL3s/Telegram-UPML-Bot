from aiogram.filters.callback_data import CallbackData


class OpenMenu(CallbackData, prefix="open"):
    """Фабрика для открытия разных меню бота."""

    menu: str
    date: str | None = None


class StateData(CallbackData, prefix="state"):
    """Фабрика для подтверждения и отмены в состояниях."""

    action: str
