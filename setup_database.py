"""
Database setup script for AaiTech Industries
Creates database, tables, and loads data from CSV files
"""
import os
import pandas as pd
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "aaitech")


def get_connection(database=None):
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=database
    )


def create_database():
    print("Creating database...")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{MYSQL_DATABASE}`")
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✓ Database '{MYSQL_DATABASE}' ready")


def create_tables():
    print("\nCreating tables...")
    conn = get_connection(database=MYSQL_DATABASE)
    cursor = conn.cursor()

    statements = [
        """CREATE TABLE IF NOT EXISTS customers (
            customer_id VARCHAR(10) PRIMARY KEY,
            company_name VARCHAR(100),
            contact_name VARCHAR(100),
            city VARCHAR(50),
            country VARCHAR(50)
        )""",
        """CREATE TABLE IF NOT EXISTS suppliers (
            supplier_id INT PRIMARY KEY,
            company_name VARCHAR(100),
            contact_name VARCHAR(100),
            city VARCHAR(50),
            country VARCHAR(50)
        )""",
        """CREATE TABLE IF NOT EXISTS products (
            product_id INT PRIMARY KEY,
            product_name VARCHAR(100),
            supplier_id INT,
            category VARCHAR(50),
            unit_price FLOAT
        )""",
        """CREATE TABLE IF NOT EXISTS orders (
            order_id INT PRIMARY KEY,
            customer_id VARCHAR(10),
            order_date DATE,
            ship_city VARCHAR(50),
            freight FLOAT
        )""",
        """CREATE TABLE IF NOT EXISTS order_details (
            order_id INT,
            product_id INT,
            quantity INT,
            unit_price FLOAT,
            PRIMARY KEY (order_id, product_id)
        )""",
    ]

    for stmt in statements:
        cursor.execute(stmt)

    conn.commit()
    cursor.close()
    conn.close()
    print("✓ All tables created")


def load_csv_data():
    print("\nLoading CSV data...")
    conn = get_connection(database=MYSQL_DATABASE)
    cursor = conn.cursor()

    # Order matters due to foreign keys — load parents first
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_files = [
        ("customers",    os.path.join(base_dir, "data", "customers.csv")),
        ("suppliers",    os.path.join(base_dir, "data", "suppliers.csv")),
        ("products",     os.path.join(base_dir, "data", "products.csv")),
        ("orders",       os.path.join(base_dir, "data", "orders.csv")),
        ("order_details", os.path.join(base_dir, "data", "order_details.csv")),
    ]

    for table, path in csv_files:
        if not os.path.exists(path):
            print(f"⚠  {path} not found, skipping")
            continue

        cursor.execute(f"DELETE FROM `{table}`")
        df = pd.read_csv(path)

        cols = ", ".join(f"`{c}`" for c in df.columns)
        placeholders = ", ".join(["%s"] * len(df.columns))
        sql = f"INSERT INTO `{table}` ({cols}) VALUES ({placeholders})"

        for _, row in df.iterrows():
            cursor.execute(sql, tuple(None if pd.isna(v) else v for v in row))

        conn.commit()
        print(f"✓ {table}: {len(df)} rows loaded")

    cursor.close()
    conn.close()


def verify():
    print("\nVerifying...")
    conn = get_connection(database=MYSQL_DATABASE)
    cursor = conn.cursor()
    for t in ["customers", "suppliers", "products", "orders", "order_details"]:
        cursor.execute(f"SELECT COUNT(*) FROM `{t}`")
        print(f"  {t}: {cursor.fetchone()[0]} rows")
    cursor.close()
    conn.close()


if __name__ == "__main__":
    print("=" * 50)
    print("AaiTech Industries — Database Setup")
    print("=" * 50)
    create_database()
    create_tables()
    load_csv_data()
    verify()
    print("\n✓ Setup complete!")
