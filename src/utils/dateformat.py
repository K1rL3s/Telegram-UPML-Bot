from datetime import date


def format_date(_date: date) -> str:
    """
    Формат объекта даты в вид "dd.MM.YYYY" с лидирующими нулями.

    :param _date: Объект даты.
    :return: Отформатированная строка.
    """

    return f'{_date.day:0>2}.{_date.month:0>2}.{_date.year:0>2}'


def date_by_format(_date: str) -> date:
    """
    Конвертация отформатированной строки в дату.

    :param _date: Дата в виде строки.
    :return: Объект даты.
    """

    if _date.lower() == 'today':
        return date.today()

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
