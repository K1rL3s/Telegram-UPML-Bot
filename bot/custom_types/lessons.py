from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    import datetime as dt


@dataclass
class LessonsAlbum:
    """Сборник расписаний. Дата, класс, полное расписание и для каждого класса."""

    text: str | None
    status: bool
    full_photo_id: str
    class_photo_ids: list[str]
    grade: str | None
    date: "Optional[dt.date]"
