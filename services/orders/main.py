import uuid

from fastapi import FastAPI, HTTPException, status
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


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    product_id = str(uuid.uuid4())
    products[product_id] = product
    return {"id": product_id, **product.model_dump()}


@app.get("/products", status_code=status.HTTP_200_OK)
def list_products():
    return [
        {"id": product_id, **product.model_dump()}
        for product_id, product in products.items()
    ]


@app.get("/products/{product_id}", status_code=status.HTTP_200_OK)
def get_product(product_id: str):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"id": product_id, **products[product_id].model_dump()}


@app.put("/products/{product_id}", status_code=status.HTTP_200_OK)
def update_product(product_id: str, product: Product):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    products[product_id] = product
    return {"id": product_id, **product.model_dump()}


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    del products[product_id]


@app.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(order: Order):
    for item in order.items:
        if item.product_id not in products:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item.product_id} not found",
            )
    order_id = str(uuid.uuid4())
    orders[order_id] = order
    return {"id": order_id, **order.model_dump()}
