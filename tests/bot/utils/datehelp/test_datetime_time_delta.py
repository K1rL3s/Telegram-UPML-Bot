import datetime as dt

import pytest

from bot.utils.datehelp import datetime_time_delta


class TestDatetimeTimeDeltaDatehelpTest:
    @pytest.mark.parametrize(
        "datetime, target_time, expected_result",
        (
            (
                dt.datetime(2023, 1, 1, 10, 0),
                dt.time(12, 0),
                dt.timedelta(hours=2, minutes=0),
            ),
            (
                dt.datetime(2023, 1, 1, 14, 30),
                dt.time(12, 0),
                dt.timedelta(hours=21, minutes=30),
            ),
            (
                dt.datetime(2023, 1, 1, 12, 0),
                dt.time(12, 0),
                dt.timedelta(hours=0, minutes=0),
            ),
            (
                dt.datetime(2023, 1, 1, 0, 0),
                dt.time(12, 0),
                dt.timedelta(hours=12, minutes=0),
            ),
            (
                dt.datetime(2023, 1, 1, 12, 0),
                dt.time(0, 0),
                dt.timedelta(hours=12, minutes=0),
            ),
            (
                dt.datetime(2023, 1, 1, 0, 0),
                dt.time(0, 0),
                dt.timedelta(hours=0, minutes=0),
            ),
            (
                dt.datetime(2023, 1, 1, 23, 59),
                dt.time(0, 1),
                dt.timedelta(hours=0, minutes=2),
            ),
            (
                dt.datetime(2023, 1, 1, 0, 1),
                dt.time(23, 59),
                dt.timedelta(hours=23, minutes=58),
            ),
            (
                dt.datetime(2023, 1, 1, 0, 0),
                dt.time(23, 59),
                dt.timedelta(hours=23, minutes=59),
            ),
        ),
    )
    def test_valid_datetime_time_delta(
        self,
        datetime: "dt.datetime",
        target_time: "dt.time",
        expected_result: "dt.timedelta",
    ) -> None:
        assert datetime_time_delta(datetime, target_time) == expected_result
