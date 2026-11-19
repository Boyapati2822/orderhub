from dataclasses import dataclass


@dataclass
class OrderItem:
    order_id: str
    product_id: str
    quantity: int

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
