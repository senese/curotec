from datetime import datetime
from fastapi import (
    APIRouter,
    Depends,
    status,
)
from pydantic import BaseModel, EmailStr

from app.deps.dependencies import check_content_type, get_current_user, get_session
from app.controllers.user_controller import (
    CreateUserController,
    GetUserController,
    DeleteUserController,
    UpdateUserNameController,
)


router = APIRouter()

# Create


class CreateUserInput(BaseModel):
    name: str
    email: EmailStr
    password: str


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
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
    "/me",
    response_model=GetOrUpdateUserOutput,
)
async def get_user(user_id=Depends(get_current_user), session=Depends(get_session)):
    output = GetUserController.execute(session, user_id)
    return output


# Update

class UpdateUserInput(BaseModel):
    name: str


@router.patch(
    "/",
    response_model=GetOrUpdateUserOutput,
)
async def update_user(
    input: UpdateUserInput,
    user_id=Depends(get_current_user),
    session=Depends(get_session)
):
    output = UpdateUserNameController.execute(session, input.name, user_id)
    return output


# Delete


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(user_id=Depends(get_current_user), session=Depends(get_session)):
    DeleteUserController.execute(session, user_id)
