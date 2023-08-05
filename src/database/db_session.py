import contextlib
from pathlib import Path

import sqlalchemy
import sqlalchemy.ext.declarative as dec
from sqlalchemy.orm import Session, sessionmaker
from loguru import logger


SqlAlchemyBase = dec.declarative_base()

__factory: sessionmaker | None = None


def global_init(db_file: str | Path) -> None:
    """
    Иницализация подключения к файлу базы данной.

    :param db_file: Название файла бд или путь до него.
    """

    global __factory

    if __factory:
        return

    if isinstance(db_file, str):
        db_file = db_file.strip()

    if not db_file:
        raise RuntimeError("Необходимо указать файл (путь до) базы данных.")

    conn_str = f'sqlite:///{db_file}'
    engine = sqlalchemy.create_engine(conn_str, echo=False)
    __factory = sessionmaker(bind=engine)

    logger.info(f'Подключение к базе данных успешно')

    from src.database import __all_models  # noqa

    SqlAlchemyBase.metadata.create_all(engine)


@contextlib.contextmanager
def get_session(do_commit: bool = False) -> Session:
    """
    Создатель сессии для работы с базой данных.

    :param do_commit: Делать ли коммит изменений после выхода
                      из контекстного менеджера.
    :return: Сессия SqlAlchemy.
    """

    global __factory

    if not __factory:
        raise RuntimeError("Брат, а кто global_init вызывать будет?")

    session = __factory(expire_on_commit=False)
    try:
        yield session
    except Exception as e:
        do_commit = False
        session.rollback()
        raise e
    finally:
        if do_commit:
            session.commit()
        session.close()
