from entities.entities import Order
from pydantic_core import ValidationError
import pytest


def test_order_creation():
    order = Order(
        name="Order1",
        user_id=1,
        value=10.90
    )
    assert order.id is None
    assert order.name == "Order1"
    assert order.user_id == 1
    assert order.value == 10.90


def test_id_validation():
    int_regex = "id\n( )+Input should be a valid integer"
    negative_float_regex = "Input should be greater than 0"

    with pytest.raises(ValidationError, match=int_regex):
        Order(id="")      # type: ignore
    with pytest.raises(ValidationError, match=int_regex):
        Order(id="Test")  # type: ignore
    with pytest.raises(ValidationError, match=negative_float_regex):
        Order(id=-1)      # type: ignore


def test_name_validation():
    required_regex = "name\n( )+Field required"
    error_regex = "name\n( )+String should have at least 2 characters"

    with pytest.raises(ValidationError, match=required_regex):
        Order()           # type: ignore
    with pytest.raises(ValidationError, match=error_regex):
        Order(name="")    # type: ignore


def test_value_validation():
    required_regex = "value\n( )+Field required"
    error_regex = "value\n( )+Input should be a valid number"
    negative_float_regex = "Input should be greater than 0"

    with pytest.raises(ValidationError, match=required_regex):
        Order()                   # type: ignore
    with pytest.raises(ValidationError, match=error_regex):
        Order(value="")       # type: ignore
    with pytest.raises(ValidationError, match=negative_float_regex):
        Order(value="-10")    # type: ignore
    with pytest.raises(ValidationError, match=negative_float_regex):
        Order(value=-10)      # type: ignore
