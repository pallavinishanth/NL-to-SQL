"""Run this once to create and seed the sample SQLite database."""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "store.db")


def setup():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS order_items;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS customers;
        DROP TABLE IF EXISTS categories;

        CREATE TABLE categories (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );

        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category_id INTEGER REFERENCES categories(id),
            price REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            city TEXT,
            joined_date TEXT
        );

        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER REFERENCES customers(id),
            order_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending'
        );

        CREATE TABLE order_items (
            id INTEGER PRIMARY KEY,
            order_id INTEGER REFERENCES orders(id),
            product_id INTEGER REFERENCES products(id),
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL
        );
    """)

    cur.executemany("INSERT INTO categories VALUES (?, ?)", [
        (1, "Electronics"),
        (2, "Clothing"),
        (3, "Books"),
        (4, "Home & Kitchen"),
    ])

    cur.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?)", [
        (1, "Wireless Headphones", 1, 89.99, 150),
        (2, "Mechanical Keyboard", 1, 129.99, 80),
        (3, "USB-C Hub",           1, 45.99,  200),
        (4, "Running Shoes",       2, 74.99,  300),
        (5, "Winter Jacket",       2, 149.99, 120),
        (6, "Python Crash Course", 3, 29.99,  500),
        (7, "Clean Code",          3, 34.99,  400),
        (8, "Air Fryer",           4, 59.99,  90),
        (9, "Coffee Maker",        4, 79.99,  110),
        (10, "Yoga Mat",           4, 24.99,  250),
    ])

    cur.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?)", [
        (1,  "Alice Johnson",  "alice@email.com",   "New York",     "2023-01-15"),
        (2,  "Bob Smith",      "bob@email.com",     "Los Angeles",  "2023-03-22"),
        (3,  "Carol White",    "carol@email.com",   "Chicago",      "2023-05-10"),
        (4,  "David Brown",    "david@email.com",   "Houston",      "2023-07-04"),
        (5,  "Emma Davis",     "emma@email.com",    "Phoenix",      "2023-08-19"),
        (6,  "Frank Miller",   "frank@email.com",   "San Antonio",  "2023-09-30"),
        (7,  "Grace Wilson",   "grace@email.com",   "San Diego",    "2023-11-11"),
        (8,  "Henry Moore",    "henry@email.com",   "Dallas",       "2024-01-05"),
        (9,  "Ivy Taylor",     "ivy@email.com",     "San Jose",     "2024-02-14"),
        (10, "Jack Anderson",  "jack@email.com",    "Austin",       "2024-03-20"),
    ])

    cur.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", [
        (1,  1,  "2024-01-10", "delivered"),
        (2,  2,  "2024-01-15", "delivered"),
        (3,  3,  "2024-02-01", "delivered"),
        (4,  1,  "2024-02-14", "delivered"),
        (5,  4,  "2024-02-20", "delivered"),
        (6,  5,  "2024-03-05", "delivered"),
        (7,  2,  "2024-03-18", "delivered"),
        (8,  6,  "2024-04-01", "delivered"),
        (9,  7,  "2024-04-10", "delivered"),
        (10, 3,  "2024-04-22", "delivered"),
        (11, 8,  "2024-05-01", "delivered"),
        (12, 9,  "2024-05-08", "delivered"),
        (13, 10, "2024-05-12", "pending"),
        (14, 1,  "2024-05-13", "pending"),
        (15, 5,  "2024-05-14", "shipped"),
    ])

    cur.executemany("INSERT INTO order_items VALUES (?, ?, ?, ?, ?)", [
        (1,  1,  1,  1, 89.99),
        (2,  1,  6,  2, 29.99),
        (3,  2,  4,  1, 74.99),
        (4,  2,  10, 1, 24.99),
        (5,  3,  2,  1, 129.99),
        (6,  3,  3,  2, 45.99),
        (7,  4,  5,  1, 149.99),
        (8,  4,  7,  1, 34.99),
        (9,  5,  8,  1, 59.99),
        (10, 5,  9,  1, 79.99),
        (11, 6,  1,  1, 89.99),
        (12, 6,  2,  1, 129.99),
        (13, 7,  6,  3, 29.99),
        (14, 8,  4,  2, 74.99),
        (15, 8,  5,  1, 149.99),
        (16, 9,  3,  1, 45.99),
        (17, 9,  10, 2, 24.99),
        (18, 10, 7,  2, 34.99),
        (19, 10, 8,  1, 59.99),
        (20, 11, 9,  1, 79.99),
        (21, 11, 1,  1, 89.99),
        (22, 12, 2,  1, 129.99),
        (23, 12, 6,  1, 29.99),
        (24, 13, 5,  1, 149.99),
        (25, 14, 3,  1, 45.99),
        (26, 15, 4,  1, 74.99),
        (27, 15, 10, 3, 24.99),
    ])

    conn.commit()
    conn.close()
    print(f"Database created at: {DB_PATH}")


if __name__ == "__main__":
    setup()
