import uuid

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel


class Product(BaseModel):
    name: str
    unit_price: float


class OrderItem(BaseModel):
    product_id: str
    quantity: int


class Order(BaseModel):
    items: list[OrderItem]


app = FastAPI()
products: dict[str, Product] = {}
orders: dict[str, Order] = {}


def get_product_store() -> dict[str, Product]:
    return products


def get_order_store() -> dict[str, Order]:
    return orders


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(
    product: Product,
    store: dict[str, Product] = Depends(get_product_store),
):
    for existing in store.values():
        if existing.name == product.name:
            raise HTTPException(status_code=409, detail="Product name already exists")
    product_id = str(uuid.uuid4())
    store[product_id] = product
    return {"id": product_id, **product.model_dump()}


@app.get("/products", status_code=status.HTTP_200_OK)
def list_products(store: dict[str, Product] = Depends(get_product_store)):
    return [
        {"id": product_id, **product.model_dump()}
        for product_id, product in store.items()
    ]


@app.get("/products/{product_id}", status_code=status.HTTP_200_OK)
def get_product(
    product_id: str,
    store: dict[str, Product] = Depends(get_product_store),
):
    if product_id not in store:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"id": product_id, **store[product_id].model_dump()}


@app.put("/products/{product_id}", status_code=status.HTTP_200_OK)
def update_product(
    product_id: str,
    product: Product,
    store: dict[str, Product] = Depends(get_product_store),
):
    if product_id not in store:
        raise HTTPException(status_code=404, detail="Product not found")
    store[product_id] = product
    return {"id": product_id, **product.model_dump()}


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: str,
    store: dict[str, Product] = Depends(get_product_store),
):
    if product_id not in store:
        raise HTTPException(status_code=404, detail="Product not found")
    del store[product_id]


@app.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(
    order: Order,
    product_store: dict[str, Product] = Depends(get_product_store),
    order_store: dict[str, Order] = Depends(get_order_store),
):
    for item in order.items:
        if item.product_id not in product_store:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item.product_id} not found",
            )
    order_id = str(uuid.uuid4())
    order_store[order_id] = order
    return {"id": order_id, **order.model_dump()}


@app.get("/orders/{order_id}", status_code=status.HTTP_200_OK)
def get_order(
    order_id: str,
    store: dict[str, Order] = Depends(get_order_store),
):
    if order_id not in store:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"id": order_id, **store[order_id].model_dump()}
