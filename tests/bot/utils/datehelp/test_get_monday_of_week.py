import datetime as dt
from typing import TYPE_CHECKING

from bot.utils.datehelp import date_today, get_monday_of_week

if TYPE_CHECKING:
    from bot.settings import Settings


class TestGetMondayOfWeek:
    def test_if_no_date_provided(self, settings: "Settings") -> None:
        today = date_today(settings.other.timezone_offset)
        timedelta = dt.timedelta(days=today.weekday())
        expected_date = today - timedelta
        assert get_monday_of_week(None, settings.other.timezone_offset) == expected_date

    def test_if_date_provided(self) -> None:
        wednesday = dt.date(2023, 10, 4)
        monday = dt.date(2023, 10, 2)
        assert get_monday_of_week(wednesday) == monday

    def test_date_is_monday(self) -> None:
        monday = dt.date(2023, 10, 2)
        assert get_monday_of_week(monday, timezone_offset=0) == monday

    def test_date_is_sunday(self) -> None:
        sunday = dt.date(2023, 10, 8)
        monday = dt.date(2023, 10, 2)
        assert get_monday_of_week(sunday) == monday

    def test_earliest_possible_date(self) -> None:
        provided_date = dt.date.min
        expected_date = provided_date - dt.timedelta(days=provided_date.weekday())
        assert get_monday_of_week(provided_date) == expected_date

    def test_leap_year(self) -> None:
        tuesday = dt.date(2024, 2, 29)
        monday = dt.date(2024, 2, 26)
        assert get_monday_of_week(tuesday) == monday

    def test_date_divisible_by_100_not_by_400(self) -> None:
        friday = dt.date(2100, 1, 1)
        monday = dt.date(2099, 12, 28)
        assert get_monday_of_week(friday) == monday
