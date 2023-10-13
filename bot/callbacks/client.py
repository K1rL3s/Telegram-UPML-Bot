from aiogram.filters.callback_data import CallbackData


class LaundryData(CallbackData, prefix="laundry"):
    """CallbackData для таймеров прачечной."""

    action: str
    attr: str | None = None


class SettingsData(CallbackData, prefix="settings"):
    """CallbackData для настроек."""

    action: str
    attr: str | None = None
