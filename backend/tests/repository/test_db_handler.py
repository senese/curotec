from sqlalchemy import Engine
from sqlalchemy.orm import Session
from repository.db_handler import DBConnectionHandler


DB_URL = "sqlite:///:memory:"


def test_db_connection_handler():
    with DBConnectionHandler(DB_URL) as db:
        assert isinstance(db.engine, Engine)
        assert isinstance(db.session, Session)
        assert db.session.bind.url.database == ":memory:"
        assert db.session.bind.url.drivername == "sqlite"
