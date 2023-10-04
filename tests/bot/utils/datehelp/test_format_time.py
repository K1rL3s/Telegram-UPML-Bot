import datetime as dt
from typing import Any

import pytest

from bot.utils.datehelp import format_time


class TestFormatTimeDatehelpTest:
    @pytest.mark.parametrize(
        "time, result",
        (
            (dt.time(9, 5), "09:05"),
            (dt.time(15, 30), "15:30"),
            (dt.time(0, 45), "00:45"),
            (dt.time(10, 0), "10:00"),
            (dt.time(23, 59), "23:59"),
            (dt.time(12, 30, 45, 500000), "12:30"),
            (dt.datetime(2021, 1, 1, 10, 30), "10:30"),
            (dt.datetime(2022, 1, 1, 12, 30, tzinfo=dt.timezone.utc).time(), "12:30"),
        ),
    )
    def test_valid_format_time(self, time: "dt.time", result: str) -> None:
        assert format_time(time) == result

    @pytest.mark.parametrize(
        "time, exception",
        (
            (None, AttributeError),
            ("12:30", AttributeError),
        ),
    )
    def test_invalid_format_time(self, time: Any, exception: type[Exception]) -> None:
        with pytest.raises(exception):
            format_time(time)
