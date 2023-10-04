import datetime as dt

import pytest

from bot.utils.datehelp import weekday_by_date


class TestWeekdayByDateDatehelpTest:
    @pytest.mark.parametrize(
        "date, weekday",
        (
            (dt.date(2023, 1, 2), "понедельник"),
            (dt.date(2023, 1, 3), "вторник"),
            (dt.date(2023, 1, 4), "среда"),
            (dt.date(2023, 1, 5), "четверг"),
            (dt.date(2023, 1, 6), "пятница"),
            (dt.date(2023, 1, 7), "суббота"),
            (dt.date(2023, 1, 8), "воскресенье"),
            (dt.date(1, 1, 1), "понедельник"),
            (dt.date(2020, 2, 29), "суббота"),
            (dt.date(2022, 2, 15), "вторник"),
        ),
    )
    def test_valid_weekday_by_date(self, date: "dt.date", weekday: str) -> None:
        assert weekday_by_date(date) == weekday
