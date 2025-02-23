from fastapi import Request, HTTPException
from repository.db_handler import DBConnectionHandler
import os

# In a bigger project, environment variables should be loaded inside a Config class
DB_URL = os.getenv("DB_URL", "sqlite:///test.db")


def check_content_type(request: Request):
    if request.headers.get("content-type") != "application/json":
        raise HTTPException(
            status_code=415, detail="Wrong Content-Type. Please use application/json"
        )


def get_session():
    with DBConnectionHandler(DB_URL) as db:
        return db.session
