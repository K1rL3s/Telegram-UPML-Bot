import datetime as dt
from typing import Union

from bot.settings import get_settings
from bot.utils.consts import TODAY


# Смещение часового пояса по умолчанию, используется при работе бота.
# В тестах всегда должно подставляться одинаковое значение.
default_timezone_offset = get_settings().other.TIMEZONE_OFFSET


def format_date(date: "dt.date", with_year: bool = True) -> str:
    """
    Формат объекта даты в вид "dd.MM.YYYY" с лидирующими нулями.

    :param date: Объект даты.
    :param with_year: Вернуть строку годом или без.
    :return: Отформатированная строка.
    """
    return date.strftime("%d.%m.%Y") if with_year else date.strftime("%d.%m")


def format_datetime(datetime: "dt.datetime") -> str:
    """
    Формат объекта даты и времени в вид "dd.MM.YYYY hh:mm:ss" с лидирующими нулями.

    :param datetime: Объект даты и времени.
    :return: Отформатированная строка.
    """
    return datetime.strftime("%d.%m.%Y %H:%M:%S")


def date_by_format(
    date: str,
    timezone_offset: int = default_timezone_offset,
) -> "Union[dt.date, bool]":
    """
    Конвертация отформатированной строки в дату.

    :param date: Дата в виде строки, день-месяц-год через тире, точку или пробел.
    :param timezone_offset: Смещение часового пояса в часах.
    :return: Объект даты.
    """
    if date.lower() == TODAY:
        return date_today(timezone_offset)

    date = date.replace("-", " ").replace(".", " ")
    try:
        day, month, year = map(int, date.strip().split())

        if year < 1000:  # Если не ГГГГ, а ГГ
            year += date_today().year // 1000 * 1000

        date_obj = dt.date(day=day, month=month, year=year)
    except ValueError:
        return False
    return date_obj


def hours_minutes_to_minutes(text: str) -> int:
    """
    Строка формата "{часы} {минуты}" в минуты, разделитель точка, запятая или пробел.

    :param text: Сообщение пользователя.
    :return: Минуты.
    """
    hours, minutes = map(int, text.replace(",", " ").replace(".", " ").split())
    return hours * 60 + minutes


def minutes_to_hours_minutes(minutes: int) -> tuple[int, int]:
    """
    Формат минут в часы и минуты.

    :param minutes: Минуты.
    :return: Часы и минуты.
    """
    hours = minutes // 60
    minutes -= hours * 60
    return hours, minutes


def weekday_by_date(date_: "dt.date") -> str:
    """
    День недели по дате.

    :param date_: Объект даты.
    :return: День недели в виде строки.
    """
    return (
        "понедельник",
        "вторник",
        "среда",
        "четверг",
        "пятница",
        "суббота",
        "воскресенье",
    )[date_.weekday()]


def get_this_week_monday(timezone_offset: int = default_timezone_offset) -> "dt.date":
    """
    Возвращает объект date с понедельником текущей недели.

    :param timezone_offset: Смещение часового пояса в часах.
    :return: date.
    """
    today = date_today(timezone_offset)
    return today - dt.timedelta(days=today.weekday())


def datetime_now(timezone_offset: int = default_timezone_offset) -> "dt.datetime":
    """
    Функция datetime.datetime.now, но в указанной в ``.env`` временной зоне.

    :param timezone_offset: Смещение часового пояса в часах.
    :return: datetime.
    """
    return dt.datetime.now(
        tz=dt.timezone(offset=dt.timedelta(hours=timezone_offset)),
    ).replace(tzinfo=None)


def date_today(timezone_offset: int = default_timezone_offset) -> "dt.date":
    """
    Функция datetime.date.today, но в указанной в ``.env`` временной зоне.

    :param timezone_offset: Смещение часового пояса в часах.
    :return: date.
    """
    return datetime_now(timezone_offset).date()
