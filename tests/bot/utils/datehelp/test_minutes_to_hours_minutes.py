import pytest

from bot.utils.datehelp import minutes_to_hours_minutes


class TestMinutesToHoursMinutesDatehelpTest:
    @pytest.mark.parametrize(
        "minutes, hours_minutes",
        (
            (0, (0, 0)),
            (59, (0, 59)),
            (120, (2, 0)),
            (1440, (24, 0)),
            (60, (1, 0)),
            (61, (1, 1)),
            (719, (11, 59)),
            (720, (12, 0)),
            (721, (12, 1)),
        ),
    )
    def test_valid_minutes_to_hours_minutes(
        self,
        minutes: int,
        hours_minutes: tuple[int, int],
    ) -> None:
        assert minutes_to_hours_minutes(minutes) == hours_minutes

    @pytest.mark.parametrize("minutes, exception", ((-1, ValueError),))
    def test_invalid_minutes_to_hours_minutes(
        self,
        minutes: int,
        exception: type[Exception],
    ) -> None:
        with pytest.raises(exception):
            minutes_to_hours_minutes(minutes)
