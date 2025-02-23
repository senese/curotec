from repository.user.user_model import UserModel
from repository.order.order_repository import OrderRepository
from repository.order.order_model import OrderModel
from entities.entities import Order
from sqlalchemy.orm import InstanceState
from sqlalchemy.exc import NoResultFound
from datetime import datetime
import pytest
import time


@pytest.fixture
def inserted_user(db_session):
    user = UserModel(
        name="User1",
        email="teste@email.com"
    )
    db_session.add(user)
    db_session.commit()
    yield user

    db_session.delete(user)
    db_session.commit()


@pytest.fixture
def order_test(inserted_user):
    return Order(
        name="Order1",
        user_id=inserted_user.id,
        value=100
    )


def assert_model_attributes(model: OrderModel):
    expected_attrs = {
        "id": int,
        "user_id": int,
        "name": str,
        "value": int,
        "created_at": datetime,
        "updated_at": datetime,
        "_sa_instance_state": InstanceState
    }
    assert isinstance(model, OrderModel)
    assert model.__dict__.keys() == expected_attrs.keys()
    for key, expected_type in expected_attrs.items():
        response_value = model.__dict__[key]  # will raise KeyError if don't exist
        assert isinstance(response_value, expected_type)


def assert_values_against_entity(model: OrderModel, entity: Order, dt: datetime):
    entity_dict = entity.model_dump(mode="json")
    for key in entity_dict.keys():
        print(key)
        assert model.__dict__[key] == entity_dict[key]
    assert model.created_at == dt
    assert model.updated_at == dt


def test_insert_order(order_test, db_session):
    order_repository = OrderRepository(db_session)
    order_model = order_repository.insert(order_test)
    order_test.id = order_model.id

    found_order = db_session.query(OrderModel).filter(
        OrderModel.id == order_model.id
    ).one()

    # SQL Alchemy return naive UTC datetime objects
    dt = datetime.utcnow().replace(microsecond=0)
    assert_model_attributes(found_order)
    assert_values_against_entity(found_order, order_test, dt)


def test_update_order(order_test, db_session):
    order_repository = OrderRepository(db_session)
    order_model = order_repository.insert(order_test)
    order_test.id = order_model.id

    order_test.name = "AnotherName"
    order_test.value = 200

    time.sleep(1)   # to ensure different times of creation and update
    order_repository.update(order_test)

    found_order_db = db_session.query(OrderModel).filter(
        OrderModel.id == order_test.id
    ).one()

    assert isinstance(found_order_db, OrderModel)
    assert found_order_db.created_at != found_order_db.updated_at
    assert found_order_db.name == "AnotherName"
    assert found_order_db.value == 200


def test_find_order(order_test, db_session):
    order_repository = OrderRepository(db_session)
    order_model = order_repository.insert(order_test)
    order_test.id = order_model.id

    # SQL Alchemy return naive UTC datetime objects
    dt = datetime.utcnow().replace(microsecond=0)
    found_order = order_repository.find(order_test.id)

    assert_model_attributes(found_order)
    assert_values_against_entity(found_order, order_test, dt)


def test_find_unexistent_order(db_session):
    order_repository = OrderRepository(db_session)
    not_found_regex = "Order not found"

    with pytest.raises(NoResultFound, match=not_found_regex):
        order_repository.find(-1)


def test_find_all_orders(order_test, db_session):
    order_repository = OrderRepository(db_session)
    order_model = order_repository.insert(order_test)
    order_test.id = order_model.id

    # SQL Alchemy return naive UTC datetime objects
    dt1 = datetime.utcnow().replace(microsecond=0)

    order_test2 = Order(
        name="Order2",
        user_id=1,
        value=300
    )

    order_model2 = order_repository.insert(order_test2)
    order_test2.id = order_model2.id

    # SQL Alchemy return naive UTC datetime objects
    dt2 = datetime.utcnow().replace(microsecond=0)

    orders = order_repository.find_all()
    assert type(orders) is list
    assert_model_attributes(orders[0])
    assert_values_against_entity(orders[0], order_test, dt1)
    assert_values_against_entity(orders[1], order_test2, dt2)


def test_delete_order(order_test, db_session):
    order = OrderModel(**order_test.model_dump(mode="json"))
    db_session.add(order)
    db_session.commit()

    order_repository = OrderRepository(db_session)
    order_repository.delete(order)

    not_found_regex = "Order not found"
    with pytest.raises(NoResultFound, match=not_found_regex):
        order_repository.find(order_test.id)


def test_deletion_cascade(db_session):
    user = UserModel(
        name="User1",
        email="teste@email.com"
    )
    db_session.add(user)
    db_session.commit()

    order = OrderModel(
        name="Order1",
        user_id=user.id,
        value=100
    )
    db_session.add(order)
    db_session.commit()

    db_session.delete(user)
    order_repository = OrderRepository(db_session)
    orders = order_repository.find_all()
    assert orders == []
