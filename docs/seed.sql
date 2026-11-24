INSERT INTO customers (name) VALUES
    ('Asha Patel'),
    ('Ben Carter'),
    ('Chloe Nguyen');

INSERT INTO products (name, unit_price) VALUES
    ('Keyboard', 49.99),
    ('Mouse', 19.50),
    ('Monitor', 199.00);

INSERT INTO orders (customer_id) VALUES
    (1),
    (2),
    (1);

INSERT INTO order_items (order_id, product_id, quantity) VALUES
    (1, 1, 1),
    (1, 2, 2),
    (2, 3, 1),
    (3, 2, 1);