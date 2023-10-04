import datetime as dt
from typing import TYPE_CHECKING

from bot.utils.datehelp import datetime_now

if TYPE_CHECKING:
    from bot.settings import Settings


class TestDatetimeNow:
    def test_specified_timezone(self) -> None:
        timezone_offset = 3
        result = datetime_now(timezone_offset)
        assert (
            result.date()
            == dt.datetime.now(
                dt.timezone(offset=dt.timedelta(hours=timezone_offset)),
            ).date()
        )

    def test_utc_plus_14(self) -> None:
        timezone_offset = 14
        result = datetime_now(timezone_offset)
        assert (
            result.date()
            == dt.datetime.now(
                dt.timezone(offset=dt.timedelta(hours=timezone_offset)),
            ).date()
        )

    def test_utc_minus_12(self) -> None:
        timezone_offset = -12
        result = datetime_now(timezone_offset)
        assert (
            result.date()
            == dt.datetime.now(
                dt.timezone(offset=dt.timedelta(hours=timezone_offset)),
            ).date()
        )

    def test_utc_plus_13_45(self) -> None:
        timezone_offset = 13.75
        result = datetime_now(timezone_offset)
        assert (
            result.date()
            == dt.datetime.now(
                dt.timezone(offset=dt.timedelta(hours=timezone_offset)),
            ).date()
        )

    def test_utc_minus_11_30(self) -> None:
        timezone_offset = -11.5
        result = datetime_now(timezone_offset)
        assert (
            result.date()
            == dt.datetime.now(
                dt.timezone(offset=dt.timedelta(hours=timezone_offset)),
            ).date()
        )

    def test_datetime_now_utc_plus_12(self) -> None:
        timezone_offset = 12
        expected_datetime = datetime_now(timezone_offset)
        actual_datetime = dt.datetime.now()
        actual_datetime = actual_datetime.astimezone(
            dt.timezone(offset=dt.timedelta(hours=timezone_offset)),
        )
        actual_datetime = actual_datetime.replace(tzinfo=None)
        assert actual_datetime == expected_datetime

    def test_datetime_now(self, settings: "Settings") -> None:
        tz = dt.timezone(offset=dt.timedelta(hours=settings.other.timezone_offset))
        expected_datetime = dt.datetime.now(tz=tz).replace(tzinfo=None)
        actual_datetime = datetime_now(timezone_offset=settings.other.timezone_offset)
        assert actual_datetime == expected_datetime
