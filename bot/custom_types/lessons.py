from pydantic import BaseModel, Field


class LessonsAlbum(BaseModel):
    """Сборник расписаний. Дата, класс, полное расписание и для каждого класса."""

    full_photo_id: str
    text: str | None = None
    status: bool = False
    class_photos: list[str] = Field(default_factory=list)
    class_photo_ids: list[str] = Field(default_factory=list)
    grade: str | None = None
    date: str | None = None
