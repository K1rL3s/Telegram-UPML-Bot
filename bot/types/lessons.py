import datetime as dt
from io import BytesIO

from pydantic import BaseModel, Field


class LessonsProcess(BaseModel, arbitrary_types_allowed=True):  # BytesIO :(
    """
    Информация из обработки расписания.

    Используется для промежуточного сохранения даты и параллели.
    """

    date: dt.date | None = None
    grade: str | None = None
    class_lessons: list[BytesIO] = Field(default_factory=list)


class LessonsCollection(BaseModel):
    """
    Сборник расписаний одной даты и параллели.

    Дата, параллель, полное расписание и для каждого класса.
    """

    full_photo_id: str
    text: str | None = None
    status: bool = False
    class_photos: list[str] = Field(default_factory=list)
    class_photo_ids: list[str] = Field(default_factory=list)
    grade: str | None = None
    date: str | None = None
