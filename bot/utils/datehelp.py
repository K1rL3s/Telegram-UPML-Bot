from datetime import date, datetime, timedelta, timezone

from bot.settings import Settings


def format_date(date_: date) -> str:
    """
    Формат объекта даты в вид "dd.MM.YYYY" с лидирующими нулями.

    :param date_: Объект даты.
    :return: Отформатированная строка.
    """

    return f"{date_.day:0>2}.{date_.month:0>2}.{date_.year}"


def format_datetime(datetime_: datetime) -> str:
    """
    Формат объекта даты и времени в вид "dd.MM.YYYY hh:mm:ss"
    с лидирующими нулями.

    :param datetime_: Объект даты и времени.
    :return: Отформатированная строка.
    """

    return (
        f"{datetime_.day:0>2}.{datetime_.month:0>2}.{datetime_.year} "
        f"{datetime_.hour:0>2}:{datetime_.minute:0>2}:{datetime_.second:0>2}"
    )


def date_by_format(date_: str) -> date | bool:
    """
    Конвертация отформатированной строки в дату.

    :param date_: Дата в виде строки.
    :return: Объект даты.
    """

    if date_.lower() == "today":
        return date_today()

    date_ = date_.replace("-", " ").replace(".", " ")
    try:
        day, month, year = map(int, date_.strip().split())
        date_obj = date(day=day, month=month, year=year)
    except ValueError:
        return False
    return date_obj


def weekday_by_date(date_: date) -> str:
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


def get_this_week_monday() -> date:
    """
    Возвращает объект date с понедельником текущей недели.

    :return: date.
    """

    today = date_today()
    return today - timedelta(days=today.weekday())


def datetime_now() -> datetime:
    """
    Функция datetime.datetime.now, но в указанной в ``.env`` временной зоне.

    :return: datetime.
    """
    return datetime.now(
        tz=(timezone(offset=timedelta(hours=Settings.TIMEZONE_OFFSET)))
    ).replace(tzinfo=None)


def date_today() -> date:
    """
    Функция datetime.date.today, но в указанной в ``.env`` временной зоне.

    :return: date.
    """
    return datetime_now().date()
