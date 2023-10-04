import datetime as dt
from typing import TYPE_CHECKING

import pytest

from bot.utils.datehelp import date_by_format, date_today

if TYPE_CHECKING:
    from bot.settings import Settings


class TestDateByFormatDatehelpTest:
    @pytest.mark.parametrize(
        "date, result",
        (
            ("01-02-2023", dt.date(2023, 2, 1)),
            ("01.02.2024", dt.date(2024, 2, 1)),
            ("01 02 2025", dt.date(2025, 2, 1)),
            ("31-12-999", dt.date(2999, 12, 31)),
        ),
    )
    def test_valid_date_dd_mm_yyyy(self, date: str, result: "dt.date") -> None:
        assert date_by_format(date) == result

    @pytest.mark.parametrize(
        "date, result",
        (
            ("1-2-23", dt.date(2023, 2, 1)),
            ("1.2.24", dt.date(2024, 2, 1)),
            ("1 2 25", dt.date(2025, 2, 1)),
        ),
    )
    def test_valid_date_d_m_yy(self, date: str, result: "dt.date") -> None:
        assert date_by_format(date) == result

    @pytest.mark.parametrize(
        "date, result",
        (
            ("2023-01-01", False),
            ("32-01-2024", False),
            ("01-13-2025", False),
            ("", False),
        ),
    )
    def test_invalid_date_format(self, date: str, result: bool) -> None:
        assert date_by_format("2026-01-01") is False

    def test_valid_date_today(self, settings: "Settings") -> None:
        timezone_offset = settings.other.timezone_offset

        expected_date = date_today(timezone_offset)
        for date in ("today", "TODAY", "tOdaY"):
            assert date_by_format(date, timezone_offset) == expected_date
