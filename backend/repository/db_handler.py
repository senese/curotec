from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


class Base(DeclarativeBase):
    pass


class DBConnectionHandler:
    """
    This class acts as a context manager for the database connection by
    providing a session object to the caller and closing the session when
    exiting the context.

    Params:
        db_url (str): The database URL to connect to.
    """

    def __init__(self, db_url: str) -> None:
        self.__connection_string = db_url
        self.__engine = self.__create_database_engine()
        self.__create_tables()

    def __create_database_engine(self):
        return create_engine(self.__connection_string)

    def __create_tables(self):
        Base.metadata.create_all(bind=self.__engine)

    def __enter__(self):
        SessionLocal = sessionmaker(
            bind=self.__engine,
            autocommit=False,
            autoflush=False
        )
        self.session = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    @property
    def engine(self):
        return self.__engine
