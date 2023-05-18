from datetime import date, datetime, timedelta

from src.utils.consts import Config


def format_date(_date: date) -> str:
    """
    Формат объекта даты в вид "dd.MM.YYYY" с лидирующими нулями.

    :param _date: Объект даты.
    :return: Отформатированная строка.
    """

    return f'{_date.day:0>2}.{_date.month:0>2}.{_date.year}'


def format_datetime(_datetime: datetime) -> str:
    """
    Формат объекта даты и времени в вид "dd.MM.YYYY hh:mm:ss"
    с лидирующими нулями.

    :param _datetime: Объект даты и времени.
    :return: Отформатированная строка.
    """

    return f'{_datetime.day:0>2}.{_datetime.month:0>2}.{_datetime.year} ' \
           f'{_datetime.hour:0>2}:{_datetime.minute:0>2}:{_datetime.second:0>2}'  # noqa


def date_by_format(_date: str) -> date:
    """
    Конвертация отформатированной строки в дату.

    :param _date: Дата в виде строки.
    :return: Объект даты.
    """

    if _date.lower() == 'today':
        return date_today()

    dd, mm, yyyy = map(int, _date.split('.'))
    return date(day=dd, month=mm, year=yyyy)


def weekday_by_date(_date: date) -> str:
    """
    День недели по дате.

    :param _date: Объект даты.
    :return: День недели в виде строки.
    """

    return ('понедельник', 'вторник', 'среда', 'четверг',
            'пятница', 'суббота', 'воскресенье')[_date.weekday()]


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
    return datetime.now(tz=Config.TIMEZONE).replace(tzinfo=None)


def date_today() -> date:
    """
    Функция datetime.date.today, но в указанной в ``.env`` временной зоне.

    :return: date.
    """
    return datetime_now().date()
