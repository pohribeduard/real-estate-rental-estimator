from functools import partial

from sqlalchemy import Column, create_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

from conf.settings import DATABASE_CONNECTION_STRING

Base = declarative_base()
NotNullColumn = partial(Column, nullable=False)


class BaseTable(Base):
    __abstract__ = True

    __session = None  # static instance of the session

    def __init__(self):
        """
        Setup for any table
        """
        engine = create_engine(DATABASE_CONNECTION_STRING)
        self.db_connection = engine

        BaseTable.__session = BaseTable.__session or BaseTable.__init_session(engine)  # init the session
        self.db_session = BaseTable.__session

    def _get_session(self):
        """
        Get the instance of the session
        """
        return BaseTable.session

    @staticmethod
    def __init_session(db_connection):
        """
        Init the session
        """
        session_class = sessionmaker(bind=db_connection)
        return session_class()
