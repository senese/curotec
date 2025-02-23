from pydantic import ValidationError
from entities.entities import User
import pytest


def test_user_creation():
    user = User(
        name="User",
        email="user@email.com"
    )
    assert user.id is None
    assert user.name == "User"
    assert user.email == "user@email.com"


def test_id_validation():
    int_regex = "id\n( )+Input should be a valid integer"
    negative_float_regex = "Input should be greater than 0"

    with pytest.raises(ValidationError, match=int_regex):
        User(id="")      # type: ignore
    with pytest.raises(ValidationError, match=int_regex):
        User(id="Test")  # type: ignore
    with pytest.raises(ValidationError, match=negative_float_regex):
        User(id=-1)      # type: ignore


def test_name_validation():
    required_regex = "name\n( )+Field required"
    error_regex = "name\n( )+String should have at least 2 characters"

    with pytest.raises(ValidationError, match=required_regex):
        User()              # type: ignore
    with pytest.raises(ValidationError, match=error_regex):
        User(name="")       # type: ignore


def test_email_validation():
    required_regex = "email\n( )+Field required"
    str_regex = "email\n( )+Input should be a valid string"
    error_regex = "email\n( )+value is not a valid email address: An email address must have an @-sign"
    two_at_regex = "email\n( )+value is not a valid email address: The part after the @-sign contains invalid characters: '@'"
    without_name_regex = "email\n( )+value is not a valid email address: There must be something before the @-sign"
    period_regex = "email\n( )+value is not a valid email address: An email address cannot start with a period"

    with pytest.raises(ValidationError, match=required_regex):
        User()                              # type: ignore
    with pytest.raises(ValidationError, match=error_regex):
        User(email="")                      # type: ignore
    with pytest.raises(ValidationError, match=error_regex):
        User(email="test")                  # type: ignore
    with pytest.raises(ValidationError, match=period_regex):
        User(email=".email@example.com")    # type: ignore
    with pytest.raises(ValidationError, match=two_at_regex):
        User(email="teste@oi@gmail.com")    # type: ignore
    with pytest.raises(ValidationError, match=without_name_regex):
        User(email="@outlook.com")          # type: ignore
    with pytest.raises(ValidationError, match=str_regex):
        User(email=1)                       # type: ignore
