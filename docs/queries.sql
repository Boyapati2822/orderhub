-- 1. Every order with the customer's name
SELECT o.id, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id;

-- 2. Every order item with its product name
SELECT oi.order_id, p.name, oi.quantity
FROM order_items oi
JOIN products p ON p.id = oi.product_id;

-- 3. Line total for each order item
SELECT oi.order_id, p.name, oi.quantity, oi.quantity * p.unit_price AS line_total
FROM order_items oi
JOIN products p ON p.id = oi.product_id;

-- 4. Total for each order
SELECT oi.order_id, SUM(oi.quantity * p.unit_price) AS order_total
FROM order_items oi
JOIN products p ON p.id = oi.product_id
GROUP BY oi.order_id
ORDER BY oi.order_id;

-- 5. Number of orders per customer (LEFT JOIN keeps customers with zero orders)
SELECT c.name, COUNT(o.id) AS order_count
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.name
ORDER BY c.name;

-- 6. Total spent per customer
SELECT c.name, SUM(oi.quantity * p.unit_price) AS total_spent
FROM customers c
JOIN orders o ON o.customer_id = c.id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
GROUP BY c.name
ORDER BY total_spent DESC;

-- 7. Product sold the most units
SELECT p.name, SUM(oi.quantity) AS units_sold
FROM products p
JOIN order_items oi ON oi.product_id = p.id
GROUP BY p.name
ORDER BY units_sold DESC
LIMIT 1;

-- 8. Average order total
SELECT AVG(t.order_total) AS avg_order_total
FROM (
    SELECT SUM(oi.quantity * p.unit_price) AS order_total
    FROM order_items oi
    JOIN products p ON p.id = oi.product_id
    GROUP BY oi.order_id
) t;

-- 9. Products that were never ordered
SELECT p.name
FROM products p
LEFT JOIN order_items oi ON oi.product_id = p.id
WHERE oi.id IS NULL;

-- 10. Running total of order value per customer (window function)
SELECT c.name, o.id AS order_id,
       SUM(oi.quantity * p.unit_price) AS order_total,
       SUM(SUM(oi.quantity * p.unit_price))
           OVER (PARTITION BY c.name ORDER BY o.id) AS running_total
FROM customers c
JOIN orders o ON o.customer_id = c.id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
GROUP BY c.name, o.id
ORDER BY c.name, o.id;