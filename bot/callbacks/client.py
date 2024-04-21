from aiogram.filters.callback_data import CallbackData

from shared.utils.enums import Action


class LaundryData(CallbackData, prefix="laundry"):
    """Фабрика для запуска и отмены таймеров прачечной."""

    action: str
    attr: str | None = None


class SettingsData(CallbackData, prefix="settings"):
    """Фабрика для изменения настроек."""

    action: str
    attr: str | None = None


class OlympData(CallbackData, prefix="olymp"):
    """Фабрика для открытия и изменения олимпиад."""

    action: str = Action.OPEN
    subject: str
    page: int = 0
    id: int | None = None


class UniverData(CallbackData, prefix="univer"):
    """Фабрика для открытия и изменения ВУЗов."""

    action: str = Action.OPEN
    city: str
    page: int = 0
    id: int | None = None
