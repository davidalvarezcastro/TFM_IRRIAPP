from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from settings import db_mysql_settings


engine = create_engine(
    db_mysql_settings.URI,
    convert_unicode=True,
    pool_pre_ping=True,
    pool_recycle=30
)


def get_new_connection():
    return scoped_session(sessionmaker(autocommit=False,
                                       autoflush=False,
                                       bind=engine))


@contextmanager
def session_scope():
    session = get_new_connection()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def add(self, db_session):
    try:
        db_session.add(self)
        db_session.commit()
    except Exception:
        db_session.rollback()
        raise


def update(self, db_session):
    try:
        db_session.commit()
    except Exception:
        db_session.rollback()
        raise


def delete(self, db_session):
    try:
        db_session.delete(self)
        db_session.commit()
    except Exception:
        db_session.rollback()
        raise


Base = declarative_base(name='Base')
Base.add = add
Base.delete = delete
Base.update = update
