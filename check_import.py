import py_compile, sys
try:
    py_compile.compile("app.py", doraise=True)
    print("OK - no syntax errors")
except py_compile.PyCompileError as e:
    print(f"ERROR: {e}")
