from sqlalchemy import Column, Date, Integer, String

from src.database.models.base_model import BaseModel


class ClassLessons(BaseModel):
    __tablename__ = 'class_lessons'

    id = Column(
        Integer,
        primary_key=True, autoincrement=True,
        unique=True, nullable=False
    )

    date = Column(Date, nullable=False)

    grade = Column(Integer, nullable=False)  # 10 или 11
    letter = Column(String(1), nullable=False)  # А, Б, В
    image = Column(String, nullable=False)

    def __repr__(self):
        return self._repr(
            id=self.id,
            date=self.date,
            grade=self.grade,
            letter=self.letter,
            image=self.image
        )
