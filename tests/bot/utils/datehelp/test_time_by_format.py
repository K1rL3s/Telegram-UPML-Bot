import datetime as dt

import pytest

from bot.utils.datehelp import time_by_format


class TestTimeByFormatDatehelpTest:
    @pytest.mark.parametrize(
        "time, result",
        (
            ("12:30", dt.time(hour=12, minute=30)),
            (" 12: 30 ", dt.time(hour=12, minute=30)),
            ("00:00", dt.time(hour=0, minute=0)),
            ("1:0", dt.time(hour=1, minute=0)),
            ("23:59", dt.time(hour=23, minute=59)),
        ),
    )
    def test_valid_time_string(self, time: str, result: "dt.time") -> None:
        assert time_by_format(time) == result

    @pytest.mark.parametrize(
        "time, exception",
        (
            ("24:00", ValueError),
            ("12:60", ValueError),
            ("12:ab", ValueError),
            ("12:30:00", ValueError),
            ("12-30", ValueError),
            ("12.30", ValueError),
        ),
    )
    def test_invalud_time_string(self, time: str, exception: type[Exception]) -> None:
        with pytest.raises(exception):
            time_by_format(time)
