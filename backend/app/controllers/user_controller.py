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
                name=input.name,            # type: ignore
                email=input.email,          # type: ignore
                password=input.password     # type: ignore
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
    def execute(session: Session, email_or_id: str | int):
        try:
            repository = UserRepository(session)
            if isinstance(email_or_id, str):
                model = repository.find_by_email(email_or_id)
            if isinstance(email_or_id, int):
                model = repository.find(email_or_id)

        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return model


class UpdateUserNameController:
    @staticmethod
    def execute(session: Session, name: str, user_id: int):
        try:
            repository = UserRepository(session)
            model = repository.find(user_id)
            user = User(
                id=model.id,
                name=name,
                email=model.email,
                password=model.password     # type: ignore
            )
            output = repository.update(user)
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return output


class DeleteUserController:
    @staticmethod
    def execute(session: Session, user_id: int):
        try:
            repository = UserRepository(session)
            user_model = repository.find(user_id)
            repository.delete(user_model)
        except NoResultFound:   # if doesn't exist, return Ok anyway
            pass
