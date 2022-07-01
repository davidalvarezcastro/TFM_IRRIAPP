from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from settings import db_mysql_settings

engine = create_engine(db_mysql_settings.URI, convert_unicode=True, pool_recycle=3600)


def get_new_connection():
    return scoped_session(sessionmaker(autocommit=False,
                                       autoflush=False,
                                       bind=engine))


db_session = get_new_connection()


def add(self):
    # db_session = get_new_connection()
    db_session.add(self)
    db_session.commit()


def update(self):
    # db_session = get_new_connection()
    db_session.commit()


def delete(self):
    # db_session = get_new_connection()
    db_session.delete(self)
    db_session.commit()


def query(self):
    db_session = get_new_connection()
    return db_session.query_property()


Base = declarative_base(name='Base')
Base.query = db_session.query_property()
Base.add = add
Base.delete = delete
Base.update = update
