from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from repository.db_handler import Base
import pytest


@pytest.fixture(scope='function')
def db_session():
    """
    Provide the database session. Not using `DBConnectionHandler` to not impact
    the tests if the class changes.
    """

    DATABASE_URL = "sqlite:///:memory:"

    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    yield session

    # teardown session
    session.close()
