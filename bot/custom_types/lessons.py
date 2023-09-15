from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    import datetime as dt
    from io import BytesIO


@dataclass
class LessonsAlbum:
    """Сборник расписаний. Дата, класс, полное расписание и для каждого класса."""

    full_photo_id: str
    text: str | None = None
    status: bool = False
    class_photos: list["BytesIO"] = field(default_factory=list)
    class_photo_ids: list[str] = field(default_factory=list)
    grade: str | None = None
    date: "Optional[dt.date]" = None
