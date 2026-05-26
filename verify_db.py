from database import execute_query, get_connection_status


def main() -> None:
    print("=== Connection Test ===")
    ok, err = get_connection_status()
    print("Connected:", ok)
    if not ok:
        print("Connection error:", err)

    try:
        print("\n=== Customers ===")
        df = execute_query("SELECT * FROM customers")
        print(df.to_string())

        print("\n=== Orders ===")
        df2 = execute_query("SELECT * FROM orders")
        print(df2.to_string())

        print("\n=== Dashboard Queries ===")
        df3 = execute_query("SELECT COUNT(*) as total FROM customers")
        print("Customers:", df3.iloc[0]["total"])

        df4 = execute_query("SELECT COUNT(*) as total FROM orders")
        print("Orders:", df4.iloc[0]["total"])

        df5 = execute_query(
            "SELECT ROUND(SUM(od.quantity * od.unit_price),2) as total FROM order_details od"
        )
        print("Revenue:", df5.iloc[0]["total"])

        df6 = execute_query(
            "SELECT c.country, COUNT(o.order_id) as orders "
            "FROM customers c JOIN orders o ON c.customer_id = o.customer_id "
            "GROUP BY c.country ORDER BY orders DESC"
        )
        print("\nOrders by country:")
        print(df6.to_string())
    except Exception as exc:
        print(f"Error querying database: {exc}")


if __name__ == "__main__":
    main()
