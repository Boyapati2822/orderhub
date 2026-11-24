# Journal

## 2026-11-17 (Day 1)

- Built: Set up the orderhub monorepo with uv, the tooling, and a README.
- Confused by: pip and uv 
- Open question: none

## 2026-11-19 (Day 2)

- Built: Domain models OrderItem, Customer, Product, and Order in services/orders/models.py. OrderItem rejects quantity 0 or less. Order.total() computes the total from the items and product prices. 6 pytest tests pass.

## 2026-11-19 (Day 3)

- Built: Raw HTTP server with http.server (GET, POST, 411 on missing Content-Length) and an httpx client. Findings in docs/http-notes.md.

## Day 4: FastAPI products and orders

Built FastAPI products CRUD (create, list, get, update, delete) with 404s on missing ids, plus POST /orders that rejects unknown product ids. Store is in memory for now.

## Day 5: Unit tests and first CI pipeline

Wrote pytest tests for the products and orders API with FastAPI TestClient, covering every route and its 404, 409, and 422 cases. Coverage is 100% for services/orders. Added a GitHub Actions workflow that runs ruff and pytest on every push and pull request.

## Day 6: SQL and PostgreSQL

Ran Postgres 16 with pgvector in Docker. Wrote the schema for customers, products, orders and order_items with primary and foreign keys, plus seed data and 10 practice queries (joins, GROUP BY, window function). EXPLAIN showed Hash Join and Seq Scan on the small tables. Open question: when an index on order_items.order_id starts to pay off.

## Day 7: SQLAlchemy models and Alembic migrations
Mapped the four tables (products, customers, orders, order_items) to SQLAlchemy 2 classes in services/orders/db.py. Created two Alembic migrations and applied them to the orderhub_orm database. Money uses Numeric(10,2), not float, because float cannot store decimal currency amounts exactly. The database URL comes from the DATABASE_URL value in the .env file, read by load_dotenv().
