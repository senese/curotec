from fastapi import Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import status
import jwt
import os

from app.controllers.user_controller import GetUserController
from repository.db_handler import DBConnectionHandler

# In a bigger project, environment variables should be loaded inside a Config class
DB_URL = os.getenv("DB_URL", "sqlite:///test.db")

SECRET_KEY = "892eab36714b3684fc632df3b2c7ef2616e23dc35b4fc760318ed2479b97bec8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


def check_content_type(request: Request):
    if request.headers.get("content-type") != "application/json":
        raise HTTPException(
            status_code=415, detail="Wrong Content-Type. Please use application/json"
        )


def get_session():
    with DBConnectionHandler(DB_URL) as db:
        return db.session


async def get_current_user(token=Depends(oauth2_scheme), session=Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exception

        user = GetUserController.execute(session, username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    except HTTPException:
        raise credentials_exception

    return user.id
