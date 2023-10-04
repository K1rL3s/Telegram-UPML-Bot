import datetime as dt
from typing import TYPE_CHECKING

import pytest

from bot.utils.datehelp import date_today, datetime_now

if TYPE_CHECKING:
    from bot.settings import Settings


class TestDateToday:
    def test_default_timezone(self, settings: "Settings") -> None:
        expected_date = datetime_now(settings.other.timezone_offset).date()
        assert date_today(settings.other.timezone_offset) == expected_date

    def test_valid_offset(self) -> None:
        timezone_offset = 3
        expected_date = datetime_now(timezone_offset).date()
        assert date_today(timezone_offset) == expected_date

    def test_invalid_offset(self) -> None:
        with pytest.raises(TypeError):
            date_today("invalid")

    def test_valid_float_offset(self) -> None:
        float_offset = 2.5
        expected_date = datetime_now(float_offset).date()
        assert date_today(float_offset) == expected_date

    def test_valid_negative_offset(self) -> None:
        negative_offset = -4
        expected_date = datetime_now(negative_offset).date()
        assert date_today(negative_offset) == expected_date

    def test_valid_positive_offset(self) -> None:
        positive_offset = 5
        expected_date = datetime_now(positive_offset).date()
        assert date_today(positive_offset) == expected_date

    def test_offset_0(self) -> None:
        timezone_offset = 0
        result = date_today(timezone_offset)
        assert result == dt.datetime.utcnow().date()
