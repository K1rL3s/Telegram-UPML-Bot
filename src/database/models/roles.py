from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import mapped_column

from src.database.models.base_model import BaseModel


class Role(BaseModel):
    __tablename__ = 'roles'

    id = mapped_column(
        Integer,
        primary_key=True, autoincrement=True,
        unique=True, nullable=False
    )

    role = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return self._repr(
            id=self.id,
            role=self.role
        )
