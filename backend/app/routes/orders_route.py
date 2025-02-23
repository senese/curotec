from datetime import datetime
from fastapi import (
    APIRouter,
    Depends,
    status,
)
from pydantic import BaseModel, PositiveFloat

from app.deps.dependencies import check_content_type, get_session
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
    user_id: PositiveFloat
    value: PositiveFloat


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Order,
    dependencies=[Depends(check_content_type)],
)
async def create_order(input: CreateOrderInput, session=Depends(get_session)):
    output = CreateOrderController.execute(session, input)
    return output


# Read

@router.get(
    "/",
)
async def get_orders(session=Depends(get_session)):
    orders = GetOrdersController.execute(session)
    return orders

# Update


class UpdateOrderOutput(BaseModel):
    name: str
    value: PositiveFloat
    created_at: datetime
    updated_at: datetime


@router.patch(
    "/",
    response_model=UpdateOrderOutput,
)
async def update_order(input: Order, session=Depends(get_session)):
    output = UpdateOrderController.execute(session, input)
    return output


# Delete

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_order(id: int, session=Depends(get_session)):
    output = DeleteOrderController.execute(session, id)
    return output
