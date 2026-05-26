# AaiTech AI SQL Assistant - Startup Script
Write-Host ""
Write-Host "  ============================================" -ForegroundColor Yellow
Write-Host "    AaiTech Industries - AI SQL Assistant" -ForegroundColor Yellow
Write-Host "  ============================================" -ForegroundColor Yellow
Write-Host ""

# Step 1 - Start MySQL
$mysql = Get-NetTCPConnection -LocalPort 3306 -ErrorAction SilentlyContinue
if ($mysql) {
    Write-Host "  [1/3] MySQL already running." -ForegroundColor Green
} else {
    Write-Host "  [1/3] Starting MySQL..." -ForegroundColor Cyan
    Start-Process -FilePath "C:\xampp\mysql\bin\mysqld.exe" `
        -ArgumentList "--defaults-file=C:\xampp\mysql\bin\my.ini", "--standalone" `
        -WindowStyle Minimized
    Start-Sleep -Seconds 4
    Write-Host "  MySQL started." -ForegroundColor Green
}

# Step 2 - Setup database
Write-Host "  [2/3] Setting up database..." -ForegroundColor Cyan
& "C:\ProgramData\Anaconda3\python.exe" setup_database.py
Write-Host ""

# Step 3 - Run Streamlit
Write-Host "  [3/3] Starting app..." -ForegroundColor Cyan
Write-Host ""
Write-Host "  ============================================" -ForegroundColor Yellow
Write-Host "    Open browser: http://localhost:8501" -ForegroundColor Green
Write-Host "    Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host "  ============================================" -ForegroundColor Yellow
Write-Host ""

& "C:\ProgramData\Anaconda3\python.exe" -m streamlit run app.py `
    --server.port 8501 `
    --browser.gatherUsageStats false
