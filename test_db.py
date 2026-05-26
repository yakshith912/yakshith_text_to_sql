import mysql.connector


def test_passwords(host: str = "127.0.0.1", port: int = 3306, user: str = "root") -> None:
    passwords = ["", "root", "admin", "mysql", "password", "1234", "123456", "xampp", "toor"]
    for pwd in passwords:
        try:
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=pwd,
                connection_timeout=3,
            )
            print(f"SUCCESS - root password is: '{pwd}'")
            cursor = conn.cursor()
            cursor.execute("SHOW DATABASES")
            dbs = [row[0] for row in cursor.fetchall()]
            print("Databases:", dbs)
            cursor.close()
            conn.close()
            break
        except Exception as e:
            print(f"FAILED  - '{pwd}' -> {e}")


if __name__ == "__main__":
    test_passwords()
