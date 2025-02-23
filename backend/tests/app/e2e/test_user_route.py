from typing import Any, Dict
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient
from sqlalchemy.exc import NoResultFound
from pathlib import Path
import pytest
import time
import os

from app.main import app
from entities.entities import User
from repository.user.user_model import UserModel
from repository.db_handler import DBConnectionHandler
from app.routes.users_route import router

DB_FILENAME = "test.db"
DB_URL = f"sqlite:///{DB_FILENAME}"


@pytest.fixture
def test_user():
    return User(
        name="TestUser",
        email="test@user.com"
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
        "name": str,
        "email": str,
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
        yield
        # teardown test
        try:
            user_model = db.session.query(UserModel).filter(UserModel.id == json_user["id"]).one()
            db.session.delete(user_model)
            db.session.commit()
            print(f"User {user_model.id} deleted")
        except NoResultFound:
            pass


class TestUserRouter:
    def test_user_router(self):
        route: APIRoute
        for route in router.routes:     # type: ignore
            assert route.name in ("create_user", "get_user", "update_user", "delete_user")
            match route.name:
                case 'create_user':
                    assert route.path == "/"
                    assert route.methods == {'POST'}
                case 'get_user':
                    assert route.path == "/{user_email}"
                    assert route.methods == {'GET'}
                case 'update_user':
                    assert route.path == "/"
                    assert route.methods == {'PATCH'}
                case 'delete_user':
                    assert route.path == "/{user_email}"
                    assert route.methods == {'DELETE'}


class TestCreateUser:
    def test_e2e_create_user(self, client: TestClient, test_user):
        body = {
            "name": test_user.name,
            "email": test_user.email
        }
        res = client.post("/users", json=body)
        assert res.status_code == 201
        assert res.headers.get("content-type") == "application/json"

        json_res: dict = res.json()
        assert_types_of_json_response(json_res)

    @pytest.mark.usefixtures("insert_new_user")  # use fixture without inputting as parameter
    def test_e2e_post_already_created_user(self, client: TestClient, test_user):
        body = {
            "name": test_user.name,
            "email": test_user.email
        }
        res = client.post("/users", json=body)
        assert res.status_code == 200

    def test_request_validation(self, client: TestClient):
        body = {"email": "test@email.com"}
        res = client.post("/users", json=body)
        assert res.status_code == 400
        assert res.json() == {"detail": "Field required"}

        body = {
            "name": "Test",
            "email": "test"
        }
        res = client.post("/users", json=body)
        assert res.status_code == 400
        assert res.json() == {
            "detail": "value is not a valid email address: An email address must have an @-sign."
        }


class TestGetUser:
    @pytest.mark.usefixtures("insert_new_user")
    def test_e2e_get_user(self, client: TestClient, test_user):
        res = client.get(f"/users/{test_user.email}")
        assert res.status_code == 200

        fetched_user = res.json()
        assert fetched_user["name"] == test_user.name
        assert fetched_user["email"] == test_user.email
        assert "created_at" in fetched_user
        assert "updated_at" in fetched_user

    def test_request_validation(self, client: TestClient):
        res = client.get("/users/123")
        assert res.status_code == 404
        assert res.json() == {"detail": "User not found"}


class TestUpdateUser:
    @pytest.mark.usefixtures("insert_new_user")
    def test_e2e_update_user(self, client: TestClient, test_user):
        time.sleep(1)       # to ensure different times of creation and update
        body = {
            "name": "NewName",
            "email": test_user.email
        }
        res = client.patch("/users", json=body)
        assert res.status_code == 200

        fetched_user = res.json()
        assert fetched_user["name"] == body["name"]
        assert fetched_user["created_at"] != fetched_user["updated_at"]

    def test_request_validation(self, client: TestClient):
        body = {"email": "test@email.com"}
        res = client.post("/users", json=body)
        assert res.status_code == 400
        assert res.json() == {"detail": "Field required"}

        body = {
            "name": "Test",
            "email": "test"
        }
        res = client.post("/users", json=body)
        assert res.status_code == 400
        assert res.json() == {
            "detail": "value is not a valid email address: An email address must have an @-sign."
        }


class TestDeleteUser:
    @pytest.mark.usefixtures("insert_new_user")
    def test_e2e_delete_user(self, client: TestClient, test_user):
        res = client.delete(f"/users/{test_user.email}")
        assert res.status_code == 204
