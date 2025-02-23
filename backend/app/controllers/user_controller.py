from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound

from entities.entities import User
from repository.user.user_repository import UserRepository


class CreateUserController:
    @staticmethod
    def execute(session: Session, input: BaseModel):
        try:
            user = User(
                name=input.name,    # type: ignore
                email=input.email   # type: ignore
            )
            repository = UserRepository(session)
            user_model = repository.insert(user)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f"{user.email} already exists"
            )
        return user_model


class GetUserController:
    @staticmethod
    def execute(session: Session, email: str):
        try:
            repository = UserRepository(session)
            user_model = repository.find_by_email(email)

        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user_model


class UpdateUserController:
    @staticmethod
    def execute(session: Session, input: User):
        try:
            repository = UserRepository(session)
            output = repository.update(input)
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return output


class DeleteUserController:
    @staticmethod
    def execute(session: Session, user_email: str):
        try:
            repository = UserRepository(session)
            user_model = repository.find_by_email(user_email)
            repository.delete(user_model)
        except NoResultFound:   # if doesn't exist, return Ok anyway
            pass
