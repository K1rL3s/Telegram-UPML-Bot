from aiogram.filters.callback_data import CallbackData


class LaundryData(CallbackData, prefix="laundry"):
    """Фабрика для запуска и отмены таймеров прачечной."""

    action: str
    attr: str | None = None


class SettingsData(CallbackData, prefix="settings"):
    """Фабрика для изменения настроек."""

    action: str
    attr: str | None = None


class OlympData(CallbackData, prefix="olymp"):
    """Фабрика для открытия олимпиад."""

    subject: str
    id: int | None = None
    page: int = 0


class UniverData(CallbackData, prefix="univer"):
    """Фабрика для открытия ВУЗов."""

    city: str
    id: int | None = None
    page: int = 0
