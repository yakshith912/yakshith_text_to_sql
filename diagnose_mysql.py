"""
Diagnostic tool to identify and fix MySQL connection issues.
Run this to troubleshoot error 2003: Can't connect to MySQL server.
"""

import os
import sys
import subprocess
import time
import socket
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════
# DIAGNOSTIC CHECKS
# ═══════════════════════════════════════════════════════════════════════════

def check_port_listening(host: str = "127.0.0.1", port: int = 3306) -> bool:
    """Check if the MySQL port is actually listening."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"❌ Port check failed: {e}")
        return False


def check_xampp_exists() -> bool:
    """Check if XAMPP MySQL exists."""
    paths = [
        r"C:\xampp\mysql\bin\mysqld.exe",
        r"C:\xampp\mysql\bin\my.ini",
    ]
    for path in paths:
        exists = os.path.exists(path)
        status = "✓" if exists else "✗"
        print(f"  {status} {path}")
    return all(os.path.exists(p) for p in paths)


def check_mysql_service() -> bool:
    """Check if MySQL service exists in Windows."""
    try:
        result = subprocess.run(
            ["sc", "query", "MySQL"], 
            capture_output=True, 
            text=True,
            timeout=5
        )
        running = "RUNNING" in result.stdout
        state = "RUNNING ✓" if running else "NOT RUNNING ✗"
        print(f"  MySQL Service: {state}")
        return running
    except Exception as e:
        print(f"  MySQL Service check failed: {e}")
        return False


def print_header(title: str):
    """Print a formatted section header."""
    print(f"\n{'═' * 70}")
    print(f"  {title}")
    print(f"{'═' * 70}")


# ═══════════════════════════════════════════════════════════════════════════
# SOLUTION PROVIDERS
# ═══════════════════════════════════════════════════════════════════════════

def solution_xampp():
    """Attempt to start MySQL via XAMPP."""
    print_header("SOLUTION 1: Start XAMPP MySQL")
    
    mysqld = r"C:\xampp\mysql\bin\mysqld.exe"
    myini = r"C:\xampp\mysql\bin\my.ini"
    
    if not os.path.exists(mysqld):
        print(f"❌ XAMPP not found at {mysqld}")
        print("\n   Install from: https://www.apachefriends.org")
        return False
    
    try:
        print(f"\n➜ Starting {mysqld}...")
        subprocess.Popen(
            [mysqld, f"--defaults-file={myini}", "--standalone"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        print("⏳ Waiting 5 seconds for MySQL to start...")
        time.sleep(5)
        
        if check_port_listening():
            print("✓ MySQL started successfully!")
            return True
        else:
            print("❌ MySQL started but not responding on port 3306")
            return False
    except Exception as e:
        print(f"❌ Failed to start XAMPP MySQL: {e}")
        return False


def solution_windows_service():
    """Attempt to start MySQL via Windows Service."""
    print_header("SOLUTION 2: Start MySQL Windows Service")
    
    try:
        print("\n➜ Starting MySQL80 service...")
        result = subprocess.run(
            ["net", "start", "MySQL80"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0 or "already running" in result.stdout:
            print("✓ MySQL service started successfully!")
            time.sleep(3)
            return check_port_listening()
        else:
            print(f"❌ Service start failed: {result.stdout}")
            return False
    except Exception as e:
        print(f"❌ Failed to start service: {e}")
        return False


def solution_manual():
    """Provide manual instructions."""
    print_header("SOLUTION 3: Manual Start")
    print("""
If automatic solutions failed, try manually:

1. OPTION A - Start XAMPP:
   • Open XAMPP Control Panel (C:\\xampp\\xampp-control.exe)
   • Click "Start" next to MySQL module
   
2. OPTION B - Start Windows Service:
   • Open Task Manager → Services
   • Find "MySQL80" or similar
   • Right-click → Start
   
3. OPTION C - Via Command Prompt (Admin):
   • Run: net start MySQL80
   
4. OPTION D - Via XAMPP Command Line:
   • cd C:\\xampp\\mysql\\bin
   • mysqld --defaults-file=C:\\xampp\\mysql\\bin\\my.ini --standalone
""")


def verify_connection():
    """Verify the connection works."""
    print_header("VERIFICATION: Testing Database Connection")
    
    try:
        import mysql.connector
    except ImportError:
        print("❌ mysql-connector-python not installed")
        print("   Run: pip install mysql-connector-python")
        return False
    
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="",
            connection_timeout=5
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        
        print("✓ Successfully connected to MySQL!")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


# ═══════════════════════════════════════════════════════════════════════════
# MAIN DIAGNOSTIC FLOW
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║          MySQL Connection Diagnostic Tool (Error 2003 Fix)                ║
║                                                                            ║
║  Error 2003 means: MySQL server is not running or not accessible          ║
║  This tool will diagnose and help you fix the issue                       ║
╚═══════════════════════════════════════════════════════════════════════════╝
""")

    # ─────────────────────────────────────────────────────────────────────
    # DIAGNOSTIC PHASE
    # ─────────────────────────────────────────────────────────────────────
    print_header("PHASE 1: DIAGNOSTICS")
    
    print("\n1. Checking if MySQL is listening on 127.0.0.1:3306...")
    port_listening = check_port_listening()
    print(f"   Port accessible: {'✓ YES' if port_listening else '✗ NO'}")
    
    if port_listening:
        print("\n✓ MySQL is already running! Testing database connection...")
        if verify_connection():
            print("\n🎉 Everything looks good! Your dashboard should work now.")
            return 0
        else:
            print("\n⚠️  Port is open but connection failed. Check credentials.")
            return 1
    
    print("\n2. Checking XAMPP installation...")
    xampp_exists = check_xampp_exists()
    
    print("\n3. Checking Windows MySQL Service...")
    service_running = check_mysql_service()
    
    # ─────────────────────────────────────────────────────────────────────
    # SOLUTION PHASE
    # ─────────────────────────────────────────────────────────────────────
    print_header("PHASE 2: SOLUTIONS")
    
    # Try XAMPP first
    if xampp_exists:
        if solution_xampp():
            verify_connection()
            return 0
    
    # Try Windows Service
    if solution_windows_service():
        verify_connection()
        return 0
    
    # Show manual instructions
    solution_manual()
    
    print_header("AFTER STARTING MySQL")
    print("""
Once MySQL is running:

1. Test with this script:
   python verify_db.py

2. Run the dashboard:
   streamlit run app.py

If you still get error 2003:
   • Check your MYSQL_HOST and MYSQL_PORT in .env
   • Verify MySQL is actually listening: netstat -ano | findstr 3306
   • Check firewall settings
""")
    
    return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
