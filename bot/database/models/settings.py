from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import column_property, Mapped, mapped_column, relationship

from bot.database.models.base_models import UserRelatedModel


class Settings(UserRelatedModel):
    """Модель для хранения настроек одного пользователя."""

    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False,
        unique=True,
    )

    # Класс, 10 или 11
    grade: Mapped[str] = mapped_column(String(2), default=None, nullable=True)
    # Буква класса, русская
    letter: Mapped[str] = mapped_column(String(1), default=None, nullable=True)
    # grade + letter, например, "10Б", "11А" итп
    class_: Mapped[str] = column_property(grade + letter)

    # Включены ли уведомления об обновлении расписания
    lessons_notify: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    # Включены ли уведомления новостных сообщений
    news_notify: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Сколько времени стирается бельё
    washing_time: Mapped[int] = mapped_column(
        Integer,
        default=60,
        nullable=False,
    )
    # Сколько времени сушится бельё
    drying_time: Mapped[int] = mapped_column(
        Integer,
        default=1440,
        nullable=False,
    )

    user = relationship("User", back_populates="settings", lazy="selectin")
