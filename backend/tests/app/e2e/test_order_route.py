from typing import Any, Dict
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient
from sqlalchemy.exc import NoResultFound
from pathlib import Path
import pytest
import time
import os

from repository.db_handler import DBConnectionHandler
from repository.order.order_model import OrderModel
from repository.user.user_model import UserModel
from entities.entities import Order, User
from app.routes.orders_route import router
from app.main import app

DB_FILENAME = "test.db"
DB_URL = f"sqlite:///{DB_FILENAME}"


@pytest.fixture
def test_user():
    return User(
        name="TestUser",
        email="test@user.com",
        password="Pass123"  # type: ignore
    )


@pytest.fixture
def test_order():
    return Order(
        name="TestUser",
        user_id=1,
        value=19.99
    )


@pytest.fixture
def testdb_file():
    if Path(DB_FILENAME).exists():
        os.remove('test.db')
    with open('test.db', 'x'):
        pass
        yield
        os.remove('test.db')


@pytest.fixture
def db(testdb_file):
    return DBConnectionHandler(DB_URL)


@pytest.fixture
def client():
    return TestClient(app=app)  # type: ignore


def assert_types_of_json_response(response: Dict[str, Any]):
    expected_attrs = {
        "id": int,
        "user_id": int,
        "name": str,
        "value": float,
    }
    print(response)
    assert response.keys() == expected_attrs.keys()
    for key, expected_type in expected_attrs.items():
        response_value = response[key]  # will raise KeyError if don't exist
        assert isinstance(response_value, expected_type)


@pytest.fixture
def insert_new_user(db: DBConnectionHandler, test_user):
    json_user = test_user.model_dump(mode="json")
    model_instance = UserModel(**json_user)
    with db as db:
        db.session.add(model_instance)
        db.session.commit()
        yield model_instance
        # teardown test
        try:
            user_model = db.session.query(UserModel).filter(UserModel.id == json_user["id"]).one()
            db.session.delete(user_model)
            db.session.commit()
            print(f"User {user_model.id} deleted")
        except NoResultFound:
            pass


@pytest.mark.usefixtures("insert_new_user")
@pytest.fixture
def insert_new_order(db: DBConnectionHandler, test_order):
    json_order = test_order.model_dump(mode="json")
    model_instance = OrderModel(**json_order)
    with db as db:
        db.session.add(model_instance)
        db.session.commit()
        yield model_instance
        # teardown test
        try:
            order_model = db.session.query(OrderModel).filter(OrderModel.id == model_instance.id).one()
            db.session.delete(order_model)
            db.session.commit()
            print(f"Order {order_model.id} deleted")
        except NoResultFound:
            pass


class TestOrderRouter:
    def test_order_router(self):
        route: APIRoute
        for route in router.routes:     # type: ignore
            assert route.name in ("create_order", "get_orders", "update_order", "delete_order")
            match route.name:
                case 'create_order':
                    assert route.path == "/"
                    assert route.methods == {'POST'}
                case 'get_orders':
                    assert route.path == "/"
                    assert route.methods == {'GET'}
                case 'update_order':
                    assert route.path == "/"
                    assert route.methods == {'PATCH'}
                case 'delete_order':
                    assert route.path == "/{id}"
                    assert route.methods == {'DELETE'}


class TestCreateOrder:
    def test_e2e_create_order(self, client: TestClient, insert_new_user, test_order):
        body = {
            "name": test_order.name,
            "user_id": insert_new_user.id,
            "value": test_order.value
        }
        res = client.post("/orders", json=body)
        assert res.status_code == 201
        assert res.headers.get("content-type") == "application/json"

        json_res: dict = res.json()
        assert_types_of_json_response(json_res)

    def test_request_validation(self, client: TestClient):
        body = {"name": "test"}
        res = client.post("/orders", json=body)
        assert res.status_code == 400
        assert res.json() == {"detail": "Field required"}

        body = {
            "name": "Test",
            "user_id": 1,
            "value": "test"
        }
        res = client.post("/orders", json=body)
        assert res.status_code == 400
        assert res.json() == {
            "detail": "Input should be a valid number, unable to parse string as a number"
        }


class TestGetAllOrders:
    @pytest.mark.usefixtures("insert_new_order")
    def test_e2e_get_orders(self, client: TestClient, test_order):
        res = client.get("/orders")
        assert res.status_code == 200

        fetched_order = res.json()
        assert len(fetched_order) == 1
        assert fetched_order[0]["name"] == test_order.name
        assert fetched_order[0]["value"] == test_order.value
        assert "created_at" in fetched_order[0]
        assert "updated_at" in fetched_order[0]

    def test_request_validation(self, client: TestClient):
        res = client.post("/orders/123")
        assert res.status_code == 405
        assert res.json() == {"detail": "Method Not Allowed"}


class TestUpdateOrder:
    def test_e2e_update_order(self, client: TestClient, insert_new_order):
        time.sleep(1)       # to ensure different times of creation and update
        body = {
            "id": insert_new_order.id,
            "name": "NewName",
            "user_id": 1,
            "value": 500.99
        }
        res = client.patch("/orders", json=body)
        assert res.status_code == 200

        fetched_order = res.json()
        assert fetched_order["name"] == body["name"]
        assert fetched_order["value"] == body["value"]
        assert fetched_order["created_at"] != fetched_order["updated_at"]

    def test_request_validation(self, client: TestClient, insert_new_order):
        body = {
            "id": insert_new_order.id,
            "name": "NewName",
            "user_id": 1,
        }
        res = client.patch("/orders", json=body)
        assert res.status_code == 400
        assert res.json() == {"detail": "Field required"}

        body = {
            "id": insert_new_order.id,
            "name": "Test",
            "user_id": 1,
            "value": "test"
        }
        res = client.patch("/orders", json=body)
        assert res.status_code == 400
        assert res.json() == {
            "detail": "Input should be a valid number, unable to parse string as a number"
        }


class TestDeleteOrder:
    def test_e2e_delete_order(self, client: TestClient, insert_new_order):
        res = client.delete(f"/orders/{insert_new_order.id}")
        assert res.status_code == 204
