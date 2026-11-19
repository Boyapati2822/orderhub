import pytest

from services.orders.models import Order, OrderItem, Product


def test_quantity_zero_raises_value_error():
    with pytest.raises(ValueError):
        OrderItem(order_id="o-1", product_id="p-1", quantity=0)


def test_negative_quantity_raises_value_error():
    with pytest.raises(ValueError):
        OrderItem(order_id="o-1", product_id="p-1", quantity=-2)


def test_positive_quantity_is_accepted():
    item = OrderItem(order_id="o-1", product_id="p-1", quantity=1)
    assert item.quantity == 1


def test_single_item_total():
    products = {"p-1": Product(product_id="p-1", name="Pen", unit_price=5)}
    order = Order(
        order_id="o-1",
        customer_id="c-1",
        items=[OrderItem(order_id="o-1", product_id="p-1", quantity=2)],
    )
    assert order.total(products) == 10


def test_two_items_total_adds_up():
    products = {
        "p-1": Product(product_id="p-1", name="Pen", unit_price=5),
        "p-2": Product(product_id="p-2", name="Pad", unit_price=3),
    }
    order = Order(
        order_id="o-1",
        customer_id="c-1",
        items=[
            OrderItem(order_id="o-1", product_id="p-1", quantity=2),
            OrderItem(order_id="o-1", product_id="p-2", quantity=4),
        ],
    )
    assert order.total(products) == 22


def test_empty_order_total_is_zero():
    order = Order(order_id="o-1", customer_id="c-1")
    assert order.total({}) == 0
