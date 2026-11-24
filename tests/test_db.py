from decimal import Decimal

from sqlalchemy.orm import Session

from services.orders.db import ProductRow, engine


def test_save_and_read_product():
    with Session(engine) as session:
        product = ProductRow(name="Test keyboard", unit_price=Decimal("49.99"))
        session.add(product)
        session.commit()
        product_id = product.id

    with Session(engine) as session:
        saved = session.get(ProductRow, product_id)
        assert saved.name == "Test keyboard"
        assert saved.unit_price == Decimal("49.99")
        session.delete(saved)
        session.commit()
