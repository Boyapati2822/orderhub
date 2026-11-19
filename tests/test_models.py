import pytest

from services.orders.models import OrderItem


def test_quantity_zero_raises_value_error():
    with pytest.raises(ValueError):
        OrderItem(order_id="o-1", product_id="p-1", quantity=0)


def test_negative_quantity_raises_value_error():
    with pytest.raises(ValueError):
        OrderItem(order_id="o-1", product_id="p-1", quantity=-2)


def test_positive_quantity_is_accepted():
    item = OrderItem(order_id="o-1", product_id="p-1", quantity=1)
    assert item.quantity == 1
