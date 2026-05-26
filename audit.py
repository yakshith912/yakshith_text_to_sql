import ast, sys

with open("app.py", encoding="utf-8") as f:
    src = f.read()

# 1. Syntax check
try:
    ast.parse(src)
    print("✓ Syntax OK")
except SyntaxError as e:
    print(f"✗ Syntax error: {e}")
    sys.exit(1)

# 2. Check imports exist
import importlib
for mod in ["streamlit","pandas","plotly","dotenv","openai",
            "azure.search.documents","mysql.connector"]:
    try:
        importlib.import_module(mod)
        print(f"✓ {mod}")
    except ImportError as e:
        print(f"✗ Missing: {mod} — {e}")

# 3. Check database.py exports
import database
needed = ["execute_query","test_connection"]
for fn in needed:
    if hasattr(database, fn):
        print(f"✓ database.{fn}")
    else:
        print(f"✗ database.{fn} MISSING")

# 4. Check text_to_sql.py exports
import text_to_sql
for fn in ["question_to_sql"]:
    if hasattr(text_to_sql, fn):
        print(f"✓ text_to_sql.{fn}")
    else:
        print(f"✗ text_to_sql.{fn} MISSING")

# 5. Check bad imports in app.py
bad = ["get_connection_status","MYSQL_HOST","MYSQL_PORT","MYSQL_DATABASE"]
for b in bad:
    if b in src:
        print(f"✗ Bad reference found: {b}")
    else:
        print(f"✓ No bad ref: {b}")

print("\nDone.")
