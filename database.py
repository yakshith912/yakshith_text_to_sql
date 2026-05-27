import os
import sqlite3
import subprocess
import time
from typing import Tuple
from dotenv import load_dotenv
import mysql.connector
import pandas as pd

load_dotenv()

# MySQL configuration
MYSQL_HOST     = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT     = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER     = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "aaitech")

# Connection cache and active database type selector ('mysql' or 'sqlite')
DB_TYPE = "mysql"
_conn = None


def _try_start_mysql():
    """Attempt to start XAMPP MySQL if it's not running (for local environments)."""
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


def _is_connected() -> bool:
    global _conn, DB_TYPE
    if _conn is None:
        return False
    if DB_TYPE == "mysql":
        try:
            return _conn.is_connected()
        except Exception:
            return False
    elif DB_TYPE == "sqlite":
        try:
            # SQLite connections don't have is_connected, but we can verify by running a dummy select
            _conn.execute("SELECT 1")
            return True
        except Exception:
            return False
    return False


def _create_connection(timeout: int = 5):
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        connection_timeout=timeout
    )


def _initialize_sqlite_db(conn):
    """Seed SQLite database tables from static CSV files if not already done."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='customers'")
        exists = cursor.fetchone()
        
        if not exists:
            print("SQLite: Seed tables not found. Seeding SQLite fallback database from CSV files...")
            base_dir = os.path.dirname(os.path.abspath(__file__))
            csv_files = {
                "customers": os.path.join(base_dir, "data", "customers.csv"),
                "suppliers": os.path.join(base_dir, "data", "suppliers.csv"),
                "products": os.path.join(base_dir, "data", "products.csv"),
                "orders": os.path.join(base_dir, "data", "orders.csv"),
                "order_details": os.path.join(base_dir, "data", "order_details.csv"),
            }
            
            for table_name, path in csv_files.items():
                if os.path.exists(path):
                    df = pd.read_csv(path)
                    df.to_sql(table_name, conn, if_exists='replace', index=False)
                    print(f"SQLite: Populated table '{table_name}' with {len(df)} rows.")
                else:
                    print(f"SQLite Warning: Static CSV data file not found at {path}")
            conn.commit()
    except Exception as e:
        print(f"SQLite Database Seeding failed: {e}")


def get_connection(auto_start: bool = True):
    """Create and return a active connection (MySQL with automatic SQLite fallback)."""
    global _conn, DB_TYPE
    if _is_connected():
        return _conn

    # 1. Attempt MySQL connection
    try:
        _conn = _create_connection(timeout=4)
        DB_TYPE = "mysql"
        print("Connected to MySQL Database.")
        return _conn
    except Exception as mysql_err:
        # If MySQL connection fails, try auto-starting local MySQL once (if local)
        if auto_start and "2003" in str(mysql_err) and os.name == 'nt':
            try:
                _try_start_mysql()
                _conn = _create_connection(timeout=5)
                DB_TYPE = "mysql"
                print("Connected to MySQL Database after auto-start.")
                return _conn
            except Exception:
                pass
                
        # 2. Fall back to local SQLite database
        print(f"MySQL Connection failed ({mysql_err}). Falling back to local SQLite Database...")
        try:
            DB_TYPE = "sqlite"
            db_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
            os.makedirs(db_dir, exist_ok=True)
            db_path = os.path.join(db_dir, "aaitech.db")
            
            _conn = sqlite3.connect(db_path, check_same_thread=False)
            _initialize_sqlite_db(_conn)
            return _conn
        except Exception as sqlite_err:
            raise RuntimeError(f"Database Error: Failed to connect to MySQL AND SQLite fallback: {sqlite_err}")


def execute_query(query: str) -> pd.DataFrame:
    """Execute a SQL query (MySQL or SQLite) and return results as a DataFrame."""
    conn = get_connection()
    global DB_TYPE
    
    if DB_TYPE == "sqlite":
        try:
            # SQLite does not support some MySQL specific DDLs or keywords, so clean simple conversions if any
            # For query parsing, standard SQLite handles standard SQL queries cleanly
            return pd.read_sql_query(query, conn)
        except Exception as e:
            raise RuntimeError(f"SQLite Query execution failed: {e}")
    else:
        # MySQL
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            return pd.DataFrame(rows)
        except Exception as e:
            raise RuntimeError(f"MySQL Query execution failed: {e}")
        finally:
            cursor.close()


def get_db_type() -> str:
    """Get active database type: 'mysql' or 'sqlite'."""
    get_connection(auto_start=False)
    global DB_TYPE
    return DB_TYPE


def get_connection_status() -> Tuple[bool, str]:
    """Return (reachable, status_message)."""
    try:
        conn = get_connection(auto_start=False)
        global DB_TYPE
        if DB_TYPE == "mysql":
            return True, "MySQL Connected"
        else:
            return True, "SQLite Fallback Active"
    except Exception as exc:
        return False, str(exc)


def test_connection() -> bool:
    """Return True if active database is reachable."""
    ok, _ = get_connection_status()
    return ok


if __name__ == "__main__":
    print("Testing dual database connector...")
    try:
        db_type = get_db_type()
        print(f"Active DB Type: {db_type}")
        df = execute_query("SELECT * FROM customers LIMIT 5;")
        print("Sample customers:")
        print(df)
    except Exception as e:
        print("Test Connection failed:", e)
