import pytest
from fastapi.testclient import TestClient

from services.orders.main import app, orders, products


@pytest.fixture(autouse=True)
def clear_stores():
    products.clear()
    orders.clear()
    yield


@pytest.fixture
def client():
    return TestClient(app)


def create_product(client, name="Widget", unit_price=9.5):
    response = client.post("/products", json={"name": name, "unit_price": unit_price})
    return response.json()["id"]


def test_health_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_product_returns_201(client):
    response = client.post("/products", json={"name": "Widget", "unit_price": 9.5})
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Widget"
    assert body["unit_price"] == 9.5
    assert "id" in body


def test_create_duplicate_product_name_returns_409(client):
    client.post("/products", json={"name": "Widget", "unit_price": 9.5})
    response = client.post("/products", json={"name": "Widget", "unit_price": 1.0})
    assert response.status_code == 409


@pytest.mark.parametrize("payload", [{"name": "Widget"}, {"unit_price": 9.5}, {}])
def test_invalid_product_body_returns_422(client, payload):
    response = client.post("/products", json=payload)
    assert response.status_code == 422


def test_list_products_returns_all(client):
    create_product(client, "Widget")
    create_product(client, "Gadget", 12.0)
    response = client.get("/products")
    assert response.status_code == 200
    names = sorted(p["name"] for p in response.json())
    assert names == ["Gadget", "Widget"]


def test_get_existing_product_returns_200(client):
    product_id = create_product(client)
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Widget"


def test_get_missing_product_returns_404(client):
    response = client.get("/products/does-not-exist")
    assert response.status_code == 404


def test_update_product_returns_200(client):
    product_id = create_product(client)
    response = client.put(
        f"/products/{product_id}", json={"name": "Gadget", "unit_price": 12.0}
    )
    assert response.status_code == 200
    assert response.json() == {"id": product_id, "name": "Gadget", "unit_price": 12.0}


def test_update_missing_product_returns_404(client):
    response = client.put(
        "/products/does-not-exist", json={"name": "Gadget", "unit_price": 12.0}
    )
    assert response.status_code == 404


def test_delete_product_returns_204_then_404(client):
    product_id = create_product(client)
    assert client.delete(f"/products/{product_id}").status_code == 204
    assert client.get(f"/products/{product_id}").status_code == 404


def test_create_order_returns_201(client):
    product_id = create_product(client)
    response = client.post(
        "/orders", json={"items": [{"product_id": product_id, "quantity": 2}]}
    )
    assert response.status_code == 201
    assert response.json()["items"][0]["quantity"] == 2


def test_create_order_with_unknown_product_returns_404(client):
    response = client.post(
        "/orders", json={"items": [{"product_id": "nope", "quantity": 1}]}
    )
    assert response.status_code == 404


def test_get_order_returns_200_then_404_for_missing(client):
    product_id = create_product(client)
    order_id = client.post(
        "/orders", json={"items": [{"product_id": product_id, "quantity": 2}]}
    ).json()["id"]
    assert client.get(f"/orders/{order_id}").status_code == 200
    assert client.get("/orders/does-not-exist").status_code == 404


def test_delete_missing_product_returns_404(client):
    response = client.delete("/products/does-not-exist")
    assert response.status_code == 404
