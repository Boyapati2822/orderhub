from dataclasses import dataclass, field


@dataclass
class Customer:
    customer_id: str
    name: str
    email: str


@dataclass
class Product:
    product_id: str
    name: str
    unit_price: float


@dataclass
class OrderItem:
    order_id: str
    product_id: str
    quantity: int

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than zero")


@dataclass
class Order:
    order_id: str
    customer_id: str
    items: list[OrderItem] = field(default_factory=list)

    def total(self, products: dict[str, Product]) -> float:
        return sum(
            item.quantity * products[item.product_id].unit_price for item in self.items
        )
