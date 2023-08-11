# ??
def rate_limit(limit: int, key=None):
    """
    Декоратор для настройки частоты ответа на сообщение/кнопку.

    :param limit: Раз в сколько секунд.
    :param key: Ключ/Команда.
    """

    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func

    return decorator
