CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

INSERT INTO products (name, category, price, stock)
SELECT 'Wireless Headphones', 'Electronics', 45000.00, 25
WHERE NOT EXISTS (
    SELECT 1 FROM products WHERE name = 'Wireless Headphones'
);

INSERT INTO products (name, category, price, stock)
SELECT 'Running Shoes', 'Fashion', 32000.00, 18
WHERE NOT EXISTS (
    SELECT 1 FROM products WHERE name = 'Running Shoes'
);

INSERT INTO products (name, category, price, stock)
SELECT 'Smart Watch', 'Electronics', 75000.00, 12
WHERE NOT EXISTS (
    SELECT 1 FROM products WHERE name = 'Smart Watch'
);