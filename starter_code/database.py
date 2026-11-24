"""
database.py
------------
Task 3: Build a relational database from your cleaned data.

This module covers KM-04 topics: Introduction to Databases (DBMS,
components, characteristics) and Structured Query Language (SQL).

You will use Python's built-in `sqlite3` module — no extra install
needed. SQLite stores the whole database in a single file, which makes
it perfect for a student project (and easy to include as evidence).

By the end of this file you must be able to:
  1. Create a database file (store.db) with two related tables.
  2. Insert your cleaned data into those tables.
  3. Run at least FIVE meaningful SQL queries against the data,
     including at least one JOIN and one aggregation (SUM, COUNT, AVG).
"""

import sqlite3


def get_connection(db_path: str = "store.db") -> sqlite3.Connection:
    """
    Open (and create, if needed) the SQLite database file.

    Returns:
        an open sqlite3.Connection
    """
    return sqlite3.connect(db_path)


def create_tables(conn: sqlite3.Connection) -> None:
    """
    Create the `products` and `sales` tables if they don't already exist.

    Design requirements (this IS the relational-database design task —
    think about primary keys and foreign keys, covered in KM-04 KT04):

      products
        - product_id   TEXT, PRIMARY KEY
        - product_name TEXT, NOT NULL
        - category     TEXT
        - unit_price   REAL

      sales
        - sale_id        TEXT, PRIMARY KEY
        - product_id     TEXT, FOREIGN KEY references products(product_id)
        - quantity       INTEGER
        - sale_date      TEXT   (store as 'YYYY-MM-DD')
        - payment_method TEXT
        - customer_type  TEXT
    """
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT,
            unit_price REAL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sales (
            sale_id TEXT PRIMARY KEY,
            product_id TEXT,
            quantity INTEGER,
            sale_date TEXT,
            payment_method TEXT,
            customer_type TEXT,
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
        """
    )
    conn.commit()  


def insert_products(conn: sqlite3.Connection, products_df) -> None:
    """
    Insert every row of the cleaned products DataFrame into the
    products table.

    """
    rows = [
        (
            row.product_id,
            row.product_name,
            row.category,
            row.unit_price,
        )
        for row in products_df.itertuples(index=False)
    ]
    conn.executemany(
        """
        INSERT OR REPLACE INTO products
            (product_id, product_name, category, unit_price)
        VALUES (?, ?, ?, ?)
        """,
        rows,
    )
    conn.commit()


def insert_sales(conn: sqlite3.Connection, sales_df) -> None:
    """
    Insert every row of the cleaned sales DataFrame into the sales table.

    """
    rows = [
        (
            row.sale_id,
            row.product_id,
            row.quantity,
            row.sale_date,
            row.payment_method,
            row.customer_type,
        )
        for row in sales_df.itertuples(index=False)
    ]
    conn.executemany(
        """
        INSERT OR REPLACE INTO sales
            (sale_id, product_id, quantity, sale_date, payment_method, customer_type)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        rows,
    )
    conn.commit()


# ---------------------------------------------------------------------
# SQL QUERIES — write at least FIVE for your project.
# Three are started for you below; you must complete them and add TWO
# more of your own that answer a business question you find interesting.
# ---------------------------------------------------------------------

def query_total_revenue_per_product(conn: sqlite3.Connection):
    """
    Return each product's name and its total revenue
    (quantity * unit_price, summed across all its sales),
    highest revenue first.

    """
    sql = """
    SELECT p.product_name, ROUND(SUM(s.quantity * p.unit_price), 2) AS total_revenue
    FROM sales s
    JOIN products p ON s.product_id = p.product_id
    GROUP BY p.product_name
    ORDER BY total_revenue DESC
    """
    cursor = conn.execute(sql)
    return cursor.fetchall()


def query_best_selling_product(conn: sqlite3.Connection):
    """
    Return the single product with the highest total quantity sold.

    TODO: SUM(quantity) grouped by product, ORDER BY that sum DESC, LIMIT 1.
    """
    sql = """
        SELECT p.product_name,
               SUM(s.quantity) AS total_quantity
        FROM sales AS s
        JOIN products AS p ON s.product_id = p.product_id
        GROUP BY p.product_id, p.product_name
        ORDER BY total_quantity DESC
        LIMIT 1
    """
    return conn.execute(sql).fetchall()


def query_sales_by_payment_method(conn: sqlite3.Connection):
    """
    Return the number of sales transactions per payment_method.

    TODO: COUNT(*) grouped by payment_method.
    """
    sql = """
    SELECT payment_method, COUNT(*) AS transaction_count
    FROM sales
    GROUP BY payment_method
    ORDER BY transaction_count DESC, payment_method
    """
    return conn.execute(sql).fetchall()


def query_custom_one(conn: sqlite3.Connection):
    """
    Answer: Which product category earns the most revenue?

    Joins sales to products, sums quantity times unit price, and ranks
    categories from highest to lowest revenue.
    """
    sql = """
    SELECT p.category,
           ROUND(SUM(s.quantity * p.unit_price), 2) AS category_revenue
    FROM sales AS s
    JOIN products AS p ON s.product_id = p.product_id
    GROUP BY p.category
    ORDER BY category_revenue DESC
    """
    return conn.execute(sql).fetchall()


def query_custom_two(conn: sqlite3.Connection):
    """
    Answer: What is the average basket quantity for Regular and Walk-in
    customers?

    Uses AVG() and WHERE to group only named customer types.
    """
    sql = """
    SELECT customer_type,
           ROUND(AVG(quantity), 2) AS average_quantity
    FROM sales
    WHERE customer_type IS NOT NULL
    GROUP BY customer_type
    ORDER BY average_quantity DESC
    """
    return conn.execute(sql).fetchall()
