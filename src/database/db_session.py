import contextlib
from pathlib import Path

import sqlalchemy
from loguru import logger
from sqlalchemy.orm import Session, sessionmaker
import sqlalchemy.ext.declarative as dec


SqlAlchemyBase = dec.declarative_base()

__factory: sessionmaker | None = None


def global_init(db_file: str | Path):
    global __factory

    if __factory:
        return

    if isinstance(db_file, str):
        db_file = db_file.strip()

    if not db_file:
        raise RuntimeError("Необходимо указать файл (путь до) базы данных.")

    conn_str = f'sqlite:///{db_file}'

    engine = sqlalchemy.create_engine(conn_str, echo=False)

    logger.info(f'Подключение к базе данных успешно')

    __factory = sessionmaker(bind=engine)

    from src.database import __all_models  # noqa

    SqlAlchemyBase.metadata.create_all(engine)


@contextlib.contextmanager
def create_session(do_commit: bool = False) -> Session:
    global __factory
    if not __factory:
        raise RuntimeError("Брат, а кто global_init вызывать будет?")

    session = __factory()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        if do_commit:
            session.commit()
        session.close()
