from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound

from entities.entities import Order
from repository.order.order_repository import OrderRepository


class CreateOrderController:
    @staticmethod
    def execute(session: Session, input: BaseModel, user_id: int):
        try:
            order = Order(
                name=input.name,        # type: ignore
                user_id=user_id,        # type: ignore
                value=input.value       # type: ignore
            )
            repository = OrderRepository(session)
            user_model = repository.insert(order)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f"{order.name} already exists"
            )
        return user_model


class GetOrdersController:
    @staticmethod
    def execute(session: Session, user_id: int):
        repository = OrderRepository(session)
        orders = []
        for order in repository.find_all(user_id):
            del order.user_id
            orders.append(order)
        return orders


class UpdateOrderController:
    @staticmethod
    def execute(session: Session, id: int, input: BaseModel, user_id: int):
        try:
            repository = OrderRepository(session)
            order = Order(
                id=id,                  # type: ignore
                name=input.name,        # type: ignore
                user_id=user_id,        # type: ignore
                value=input.value       # type: ignore
            )
            output = repository.update(order)
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        return output


class DeleteOrderController:
    @staticmethod
    def execute(session: Session, id: int, user_id):
        try:
            repository = OrderRepository(session)
            order_model = repository.find(id, user_id)
            repository.delete(order_model)
        except NoResultFound:   # if doesn't exist, return Ok anyway
            pass
