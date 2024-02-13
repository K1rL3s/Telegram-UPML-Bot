from aiogram.filters.callback_data import CallbackData


class LaundryData(CallbackData, prefix="laundry"):
    """Фабрика для запуска и отмены таймеров прачечной."""

    action: str
    attr: str | None = None


class SettingsData(CallbackData, prefix="settings"):
    """Фабрика для изменения настроек."""

    action: str
    attr: str | None = None


class OlympsData(CallbackData, prefix="olymps"):
    """Фабрика для открытия олимпиад."""

    subject: str
    id: int | None = None
