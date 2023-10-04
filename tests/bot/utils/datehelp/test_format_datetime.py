import datetime as dt

import pytest

from bot.utils.datehelp import format_datetime


class TestFormatDatetimeDatehelpTest:
    @pytest.mark.parametrize(
        "datetime, result",
        (
            (dt.datetime(2023, 2, 1, 12, 30, 45), "01.02.2023 12:30:45"),
            (dt.datetime(1, 1, 1, 0, 0, 0), "01.01.0001 00:00:00"),
            (dt.datetime(9999, 12, 31, 23, 59, 59), "31.12.9999 23:59:59"),
            (
                dt.datetime(2023, 1, 1, 12, 30, 45, tzinfo=dt.timezone.utc),
                "01.01.2023 12:30:45",
            ),
            (dt.datetime(2023, 1, 1, 12, 30, 45, 123456), "01.01.2023 12:30:45"),
        ),
    )
    def test_valid_format_datetime(self, datetime: "dt.datetime", result: str) -> None:
        assert format_datetime(datetime) == result
