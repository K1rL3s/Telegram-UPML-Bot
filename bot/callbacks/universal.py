from aiogram.filters.callback_data import CallbackData


class OpenMenu(CallbackData, prefix="open"):
    """CallbackData для открытия разных меню бота."""

    menu: str
    date: str | None = None


class StateData(CallbackData, prefix="state"):
    """CallbackData для подтверждения и отмены в состоянии."""

    action: str
