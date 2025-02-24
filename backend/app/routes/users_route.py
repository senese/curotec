from datetime import datetime
from fastapi import (
    APIRouter,
    Depends,
    status,
)
from pydantic import BaseModel, EmailStr

from app.deps.dependencies import check_content_type, get_session
from app.controllers.user_controller import (
    CreateUserController,
    GetUserController,
    UpdateUserController,
    DeleteUserController,
)
from entities.entities import User


router = APIRouter()

# Create


class CreateUserInput(BaseModel):
    name: str
    email: EmailStr
    password: str


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=User,
    dependencies=[Depends(check_content_type)],
)
async def create_user(input: CreateUserInput, session=Depends(get_session)):
    CreateUserController.execute(session, input)


# Read


class GetOrUpdateUserOutput(BaseModel):
    name: str
    email: str
    created_at: datetime
    updated_at: datetime


@router.get(
    "/{user_email}",
    response_model=GetOrUpdateUserOutput,
)
async def get_user(user_email: str, session=Depends(get_session)):
    output = GetUserController.execute(session, user_email)
    return output


# Update


@router.patch(
    "/",
    response_model=GetOrUpdateUserOutput,
)
async def update_user(input: User, session=Depends(get_session)):
    output = UpdateUserController.execute(session, input)
    return output


# Delete


@router.delete(
    "/{user_email}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(user_email: str, session=Depends(get_session)):
    output = DeleteUserController.execute(session, user_email)
    return output
