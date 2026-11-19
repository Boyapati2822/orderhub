# Journal

## 2026-11-17 (Day 1)

- Built: Set up the orderhub monorepo with uv, the tooling, and a README.
- Confused by: pip and uv 
- Open question: none

## 2026-11-19 (Day 2)

- Built: Domain models OrderItem, Customer, Product, and Order in services/orders/models.py. OrderItem rejects quantity 0 or less. Order.total() computes the total from the items and product prices. 6 pytest tests pass.
