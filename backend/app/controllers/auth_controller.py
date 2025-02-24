from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from fastapi.security import OAuth2PasswordRequestForm
import bcrypt
import jwt

from repository.user.user_repository import UserRepository

SECRET_KEY = "892eab36714b3684fc632df3b2c7ef2616e23dc35b4fc760318ed2479b97bec8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class LoginAuthController:

    @staticmethod
    def execute(session: Session, form_data: OAuth2PasswordRequestForm):
        user_repository = UserRepository(session)
        username = form_data.username
        password = form_data.password
        try:
            user = user_repository.find_by_email(username)
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        def passwords_are_equal():
            pwd = password.encode()
            hashed = user.password.encode()
            return bcrypt.checkpw(pwd, hashed)

        if not passwords_are_equal():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = LoginAuthController.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return access_token

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
