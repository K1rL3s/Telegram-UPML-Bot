from sqlalchemy.orm.exc import DetachedInstanceError

from bot.database.db_session import SqlAlchemyBase


class BaseModel(SqlAlchemyBase):
    __abstract__ = True

    def __repr__(self):
        return self._repr(
            **{
                c.name: getattr(self, c.name)
                for c in self.__table__.columns  # noqa
            }
        )

    def _repr(self, **fields) -> str:
        """
        Помощник __repr__, взят с https://stackoverflow.com/questions/55713664/sqlalchemy-best-way-to-define-repr-for-large-tables  
        """  # noqa

        field_strings = []
        at_least_one_attached_attribute = False

        for key, field in fields.items():
            try:
                field_strings.append(f'{key}={field!r}')
            except DetachedInstanceError:
                field_strings.append(f'{key}=DetachedInstanceError')
            else:
                at_least_one_attached_attribute = True

        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({', '.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"


class UserRelatedModel(BaseModel):
    __abstract__ = True

    user_id: int
