from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import column_property

from src.database.models.base_model import BaseModel


class ClassLessons(BaseModel):
    __tablename__ = 'class_lessons'

    id = Column(
        Integer,
        primary_key=True, autoincrement=True,
        unique=True, nullable=False
    )

    date = Column(Date, nullable=False)

    grade = Column(String(2), nullable=False)  # 10 или 11
    letter = Column(String(1), nullable=False)  # А, Б, В
    class_ = column_property(grade + letter)
    image = Column(String, nullable=False)
