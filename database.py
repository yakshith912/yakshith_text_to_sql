import os
import sqlite3
from typing import Tuple
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

# Try importing MySQL connector — not available/needed on all platforms (e.g. Render with SQLite)
try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

# MySQL configuration
MYSQL_HOST     = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT     = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER     = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "aaitech")

# Connection cache and active database type selector ('mysql' or 'sqlite')
# On Render: DB_TYPE env var is set to 'sqlite' in render.yaml
DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()
_conn = None


def _is_connected() -> bool:
    global _conn, DB_TYPE
    if _conn is None:
        return False
    if DB_TYPE == "mysql":
        if not MYSQL_AVAILABLE:
            return False
        try:
            return _conn.is_connected()
        except Exception:
            return False
    elif DB_TYPE == "sqlite":
        try:
            _conn.execute("SELECT 1")
            return True
        except Exception:
            return False
    return False


def _create_connection(timeout: int = 5):
    if not MYSQL_AVAILABLE:
        raise RuntimeError("mysql-connector-python is not installed")
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        connection_timeout=timeout
    )


def _get_sqlite_path() -> str:
    """Get the path for the SQLite database file.
    On Render: uses /tmp which is writable. Falls back to local data/ directory.
    """
    # On Render or any read-only filesystem, use /tmp for the writable DB
    if os.getenv("RENDER") == "true":
        tmp_dir = "/tmp"
        return os.path.join(tmp_dir, "aaitech.db")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_dir = os.path.join(base_dir, "data")
    os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, "aaitech.db")


def _initialize_sqlite_db(conn):
    """Seed SQLite database tables from static CSV files if not already done."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='customers'")
        exists = cursor.fetchone()
        
        if not exists:
            print("SQLite: Seeding database from CSV files...")
            # CSV files are always relative to this source file
            base_dir = os.path.dirname(os.path.abspath(__file__))
            csv_files = {
                "customers": os.path.join(base_dir, "data", "customers.csv"),
                "suppliers": os.path.join(base_dir, "data", "suppliers.csv"),
                "products": os.path.join(base_dir, "data", "products.csv"),
                "orders": os.path.join(base_dir, "data", "orders.csv"),
                "order_details": os.path.join(base_dir, "data", "order_details.csv"),
            }
            
            loaded = 0
            for table_name, path in csv_files.items():
                if os.path.exists(path):
                    df = pd.read_csv(path)
                    df.to_sql(table_name, conn, if_exists='replace', index=False)
                    loaded += 1
                    print(f"  ✓ {table_name}: {len(df)} rows")
                else:
                    print(f"  ✗ {table_name}: CSV not found at {path}")
            conn.commit()
            print(f"SQLite: {loaded}/5 tables loaded successfully.")
        else:
            print("SQLite: Tables already exist, skipping seed.")
    except Exception as e:
        print(f"SQLite seeding error: {e}")


def _connect_sqlite():
    """Create and return a SQLite connection."""
    global _conn, DB_TYPE
    DB_TYPE = "sqlite"
    db_path = _get_sqlite_path()
    _conn = sqlite3.connect(db_path, check_same_thread=False)
    _initialize_sqlite_db(_conn)
    return _conn


def get_connection(auto_start: bool = True):
    """Create and return an active connection (MySQL with automatic SQLite fallback)."""
    global _conn, DB_TYPE
    if _is_connected():
        return _conn

    # Bypass MySQL if:
    # - explicitly set to sqlite
    # - mysql connector not installed
    # - running on Render with a localhost MySQL (no MySQL on Render)
    bypass_mysql = False
    if DB_TYPE == "sqlite":
        bypass_mysql = True
    elif not MYSQL_AVAILABLE:
        bypass_mysql = True
    elif os.getenv("RENDER") == "true":
        bypass_mysql = True

    if bypass_mysql:
        print("Using SQLite database (MySQL bypassed).")
        try:
            return _connect_sqlite()
        except Exception as sqlite_err:
            raise RuntimeError(f"SQLite connection failed: {sqlite_err}")

    # 1. Attempt MySQL connection
    try:
        _conn = _create_connection(timeout=4)
        DB_TYPE = "mysql"
        print("Connected to MySQL.")
        return _conn
    except Exception as mysql_err:
        # 2. Fall back to SQLite (no XAMPP auto-start — not applicable on Render)
        print(f"MySQL unavailable ({mysql_err}). Falling back to SQLite...")
        try:
            return _connect_sqlite()
        except Exception as sqlite_err:
            raise RuntimeError(f"All databases failed. MySQL: {mysql_err} | SQLite: {sqlite_err}")


def execute_query(query: str) -> pd.DataFrame:
    """Execute a SQL query and return results as a DataFrame."""
    conn = get_connection()
    global DB_TYPE
    
    if DB_TYPE == "sqlite":
        try:
            return pd.read_sql_query(query, conn)
        except Exception as e:
            raise RuntimeError(f"SQLite query failed: {e}")
    else:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            return pd.DataFrame(rows)
        except Exception as e:
            raise RuntimeError(f"MySQL query failed: {e}")
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
        get_connection(auto_start=False)
        global DB_TYPE
        if DB_TYPE == "mysql":
            return True, "MySQL Connected"
        else:
            return True, "SQLite Active"
    except Exception as exc:
        return False, str(exc)


def test_connection() -> bool:
    """Return True if active database is reachable."""
    ok, _ = get_connection_status()
    return ok


def update_db_config(db_type: str, host: str = "127.0.0.1", port: int = 3306, user: str = "root", password: str = "", database: str = "aaitech"):
    """Update connection variables and persist them in .env file."""
    global DB_TYPE, MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, _conn
    
    # 1. Close current connection if open
    if _conn is not None:
        try:
            _conn.close()
        except Exception:
            pass
        _conn = None

    # 2. Update memory globals
    DB_TYPE = db_type.lower()
    MYSQL_HOST = host
    MYSQL_PORT = int(port)
    MYSQL_USER = user
    MYSQL_PASSWORD = password
    MYSQL_DATABASE = database

    # 3. Persist to .env
    base_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(base_dir, ".env")
    
    lines = []
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
    # Keys we want to rewrite/add
    new_values = {
        "DB_TYPE": DB_TYPE,
        "MYSQL_HOST": MYSQL_HOST,
        "MYSQL_PORT": str(MYSQL_PORT),
        "MYSQL_USER": MYSQL_USER,
        "MYSQL_PASSWORD": MYSQL_PASSWORD,
        "MYSQL_DATABASE": MYSQL_DATABASE
    }
    
    updated_lines = []
    keys_written = set()
    
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            parts = stripped.split("=", 1)
            key = parts[0].strip()
            if key in new_values:
                updated_lines.append(f"{key} = \"{new_values[key]}\"\n")
                keys_written.add(key)
                continue
        updated_lines.append(line)
        
    for key, val in new_values.items():
        if key not in keys_written:
            updated_lines.append(f"{key} = \"{val}\"\n")
            
    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)

    # 4. Force reload
    load_dotenv(override=True)


if __name__ == "__main__":
    print("Testing database connector...")
    try:
        db_type = get_db_type()
        print(f"Active DB: {db_type}")
        df = execute_query("SELECT * FROM customers LIMIT 5;")
        print(f"Customers sample ({len(df)} rows):")
        print(df)
    except Exception as e:
        print("Connection failed:", e)

