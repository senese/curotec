from datetime import datetime
from fastapi import (
    APIRouter,
    Depends,
    status,
)
from pydantic import BaseModel, PositiveFloat

from app.deps.dependencies import check_content_type, get_session, get_current_user
from app.controllers.order_controller import (
    CreateOrderController,
    GetOrdersController,
    UpdateOrderController,
    DeleteOrderController,
)
from entities.entities import Order


router = APIRouter()

# Create


class CreateOrderInput(BaseModel):
    name: str
    value: PositiveFloat


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Order,
    dependencies=[Depends(check_content_type)],
)
async def create_order(
    input: CreateOrderInput,
    session=Depends(get_session),
    user_id=Depends(get_current_user)
):
    output = CreateOrderController.execute(session, input, user_id)
    return output


# Read

@router.get(
    "/",
)
async def get_orders(
    session=Depends(get_session),
    user_id=Depends(get_current_user)
):
    orders = GetOrdersController.execute(session, user_id)
    return orders

# Update


class UpdateOrderInput(BaseModel):
    name: str
    value: PositiveFloat


class UpdateOrderOutput(BaseModel):
    name: str
    value: PositiveFloat
    created_at: datetime
    updated_at: datetime


@router.patch(
    "/{id}",
    response_model=UpdateOrderOutput,
)
async def update_order(
    id: int,
    input: UpdateOrderInput,
    session=Depends(get_session),
    user_id=Depends(get_current_user)
):
    output = UpdateOrderController.execute(session, id, input, user_id)
    return output


# Delete

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_order(
    id: int, session=Depends(get_session),
    user_id=Depends(get_current_user)
):
    DeleteOrderController.execute(session, id, user_id)
