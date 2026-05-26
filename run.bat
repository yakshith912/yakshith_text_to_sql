@echo off
title AaiTech AI SQL Assistant
color 0A

echo.
echo  ============================================
echo    AaiTech Industries - AI SQL Assistant
echo  ============================================
echo.

:: Check if MySQL already running
netstat -ano | findstr ":3306" | findstr "LISTENING" >nul 2>&1
if %errorlevel%==0 (
    echo  [1/3] MySQL already running. Skipping...
) else (
    echo  [1/3] Starting MySQL...
    start "MySQL" /MIN C:\xampp\mysql\bin\mysqld.exe --defaults-file=C:\xampp\mysql\bin\my.ini --standalone
    echo  Waiting for MySQL to start...
    ping -n 5 127.0.0.1 >nul
    echo  MySQL started.
)

echo.
echo  [2/3] Setting up database...
C:\ProgramData\Anaconda3\python.exe setup_database.py
echo.

echo  [3/3] Launching Streamlit app...
echo.
echo  ============================================
echo    Open browser at: http://localhost:8501
echo    Press Ctrl+C to stop the app
echo  ============================================
echo.

C:\ProgramData\Anaconda3\python.exe -m streamlit run app.py --server.port 8501 --browser.gatherUsageStats false

pause
