from entities.entities import Order
from repository.base_repository import BaseRepository
from .order_model import OrderModel

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from typing import List


class OrderRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def insert(self, entity: Order) -> OrderModel:
        order_dict = entity.model_dump(mode="json")
        new_order = OrderModel(**order_dict)
        self.session.add(new_order)
        self.session.commit()
        return new_order

    def update(self, entity: Order) -> OrderModel:
        model = self.find(entity.id)    # type: ignore
        model.name = entity.name
        model.value = entity.value
        self.session.commit()
        return model

    def find(self, id: int) -> OrderModel:
        try:
            order = self.session.query(OrderModel).filter_by(id=id).one()
        except NoResultFound:
            raise NoResultFound("Order not found")
        return order

    def find_all(self) -> List[OrderModel]:
        return self.session.query(OrderModel).all()

    def delete(self, model: OrderModel) -> None:
        self.session.delete(model)
        self.session.commit()
