import os
import subprocess
import time
from typing import Tuple
from dotenv import load_dotenv
import mysql.connector
import pandas as pd

load_dotenv()

MYSQL_HOST     = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT     = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER     = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "aaitech")


def _try_start_mysql():
    """Attempt to start XAMPP MySQL if it's not running."""
    try:
        mysqld = r"C:\xampp\mysql\bin\mysqld.exe"
        myini  = r"C:\xampp\mysql\bin\my.ini"
        if os.path.exists(mysqld):
            subprocess.Popen(
                [mysqld, f"--defaults-file={myini}", "--standalone"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(4)   # give it time to start
    except Exception:
        pass


_conn = None

def _is_connected() -> bool:
    return _conn is not None and _conn.is_connected()


def _create_connection(timeout: int = 5):
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        connection_timeout=timeout
    )


def get_connection(auto_start: bool = True):
    """Create and return a shared MySQL connection, auto-starting MySQL if needed."""
    global _conn
    if _is_connected():
        return _conn

    try:
        _conn = _create_connection(timeout=5)
        return _conn
    except mysql.connector.errors.InterfaceError:
        if auto_start:
            _try_start_mysql()
            # Retry once after starting
            _conn = _create_connection(timeout=8)
            return _conn
        raise


def execute_query(query: str) -> pd.DataFrame:
    """Execute a SQL query and return results as a DataFrame."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        return pd.DataFrame(rows)
    except Exception as e:
        raise RuntimeError(f"Query execution failed: {e}")
    finally:
        cursor.close()


def get_connection_status() -> Tuple[bool, str]:
    """Return (reachable, error_message)."""
    try:
        conn = get_connection()
        if not conn.is_connected():
            conn.ping(reconnect=True, attempts=2, delay=2)
        return True, ""
    except Exception as exc:
        return False, str(exc)


def test_connection() -> bool:
    """Return True if DB is reachable (auto-starts MySQL if needed)."""
    ok, _ = get_connection_status()
    return ok


if __name__ == "__main__":
    try:
        df = execute_query("SELECT * FROM customers LIMIT 5;")
        print("Sample customers:")
        print(df)
    except Exception as e:
        print("Failed:", e)
