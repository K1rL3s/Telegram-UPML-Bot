from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    import datetime as dt


@dataclass
class LessonsImage:
    """Изображение расписания уроков, нужно для обработки нераспознаных расписаний."""

    text: str | None
    status: bool
    photo_id: str
    grade: str | None
    date: "Optional[dt.date]"
