from entities.entities import User
from repository.user.user_repository import UserRepository
from repository.user.user_model import UserModel
from sqlalchemy.orm import InstanceState
from sqlalchemy.exc import NoResultFound
from datetime import datetime
import pytest
import time


@pytest.fixture
def user_test():
    return User(
        name="TestUser",
        email="test@user.com"
    )


def assert_model_attributes(model: UserModel):
    expected_attrs = {
        "id": int,
        "name": str,
        "email": str,
        "created_at": datetime,
        "updated_at": datetime,
        "_sa_instance_state": InstanceState
    }
    assert isinstance(model, UserModel)
    assert model.__dict__.keys() == expected_attrs.keys()
    for key, expected_type in expected_attrs.items():
        response_value = model.__dict__[key]  # will raise KeyError if don't exist
        assert isinstance(response_value, expected_type)


def assert_against_entity(model: UserModel, entity: User, dt: datetime):
    entity_dict = entity.model_dump(mode="json")
    for key in entity_dict.keys():
        assert model.__dict__[key] == entity_dict[key]
    assert model.created_at == dt
    assert model.updated_at == dt


def test_insert_user(user_test, db_session):
    user_repository = UserRepository(db_session)
    user_model = user_repository.insert(user_test)
    user_test.id = user_model.id

    user_found = db_session.query(UserModel).filter(
        UserModel.email == user_test.email
    ).one()

    # SQL Alchemy return naive UTC datetime objects
    dt = datetime.utcnow().replace(microsecond=0)
    assert_model_attributes(user_found)
    assert_against_entity(user_found, user_test, dt)


def test_update_user(user_test, db_session):
    user_repository = UserRepository(db_session)
    user_repository.insert(user_test)

    user_test.name = "Newname"

    time.sleep(1)   # to ensure different times of creation and update
    user_repository.update(user_test)

    user_found = db_session.query(UserModel).filter(
        UserModel.email == user_test.email
    ).one()

    assert isinstance(user_found, UserModel)
    assert user_found.name == "Newname"
    assert user_found.created_at != user_found.updated_at


def test_find_by_email(user_test, db_session):
    user_repository = UserRepository(db_session)
    user_model = user_repository.insert(user_test)
    user_test.id = user_model.id

    # SQL Alchemy return naive UTC datetime objects
    dt = datetime.utcnow().replace(microsecond=0)
    user_found = user_repository.find_by_email(user_test.email)

    assert_model_attributes(user_found)
    assert_against_entity(user_found, user_test, dt)


def test_find_unexistent_user(db_session):
    user_repository = UserRepository(db_session)
    not_found_regex = "User not found"

    with pytest.raises(NoResultFound, match=not_found_regex):
        user_repository.find(-1)


def test_find_all_users(user_test, db_session):
    user_repository = UserRepository(db_session)
    user_model = user_repository.insert(user_test)
    user_test.id = user_model.id

    # SQL Alchemy return naive UTC datetime objects
    dt1 = datetime.utcnow().replace(microsecond=0)

    user_test2 = User(
        name="User2",
        email="user2@gmail.com",
    )
    user_model2 = user_repository.insert(user_test2)
    user_test2.id = user_model2.id

    # SQL Alchemy return naive UTC datetime objects
    dt2 = datetime.utcnow().replace(microsecond=0)

    users = user_repository.find_all()
    assert type(users) is list
    assert_model_attributes(users[0])
    assert_against_entity(users[0], user_test, dt1)
    assert_against_entity(users[1], user_test2, dt2)


def test_delete_user(user_test, db_session):
    user = UserModel(**user_test.model_dump(mode="json"))
    db_session.add(user)
    db_session.commit()

    user_repository = UserRepository(db_session)
    user_repository.delete(user)

    not_found_regex = "User not found"
    with pytest.raises(NoResultFound, match=not_found_regex):
        user_repository.find(user.id)
