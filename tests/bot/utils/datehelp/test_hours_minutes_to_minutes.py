import pytest

from bot.utils.datehelp import hours_minutes_to_minutes


class TestHoursMinutesToMinutesDatehelpTest:
    @pytest.mark.parametrize(
        "hours_minutes, minutes",
        (
            ("1 30", 90),
            ("1, 30", 90),
            ("1.30", 90),
            ("0 0", 0),
            ("2,45", 165),
            ("24 0", 1440),
            ("0 60", 60),
            ("0. 60", 60),
        ),
    )
    def test_valid_hours_minutes_to_minutes(
        self,
        hours_minutes: str,
        minutes: int,
    ) -> None:
        assert hours_minutes_to_minutes(hours_minutes) == minutes

    @pytest.mark.parametrize(
        "hours_minutes, exception",
        (
            ("1.5 30", ValueError),
            ("1.5,30", ValueError),
            ("1 30,5", ValueError),
            ("0 0 0", ValueError),
        ),
    )
    def test_invalid_hours_minutes_to_minutes(
        self,
        hours_minutes: str,
        exception: type[Exception],
    ) -> None:
        with pytest.raises(exception):
            hours_minutes_to_minutes(hours_minutes)
