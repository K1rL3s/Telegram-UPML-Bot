import datetime as dt

import pytest

from bot.utils.datehelp import format_date


class TestFormatDateDatehelpTest:
    @pytest.mark.parametrize(
        "date, result",
        (
            (dt.date(2023, 11, 12), "12.11.2023"),
            (dt.date(2023, 2, 1), "01.02.2023"),
            (dt.date(1, 1, 1), "01.01.0001"),
            (dt.date(9999, 12, 31), "31.12.9999"),
        ),
    )
    def test_valid_format_date(self, date: "dt.date", result: str) -> None:
        assert format_date(date) == result

    def test_format_date_without_year(self) -> None:
        date = dt.date(2023, 2, 3)
        assert format_date(date, with_year=False) == "03.02"
