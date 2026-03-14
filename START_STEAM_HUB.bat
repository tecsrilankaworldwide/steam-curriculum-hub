@echo off
REM STEAM Curriculum Hub - Windows Startup Script

echo ========================================
echo STEAM Curriculum Hub - Sinhala Edition
echo TEC Sri Lanka Worldwide
echo ========================================
echo.

REM Check Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker Desktop not installed!
    echo Download from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo [1/3] Checking Docker Desktop...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker Desktop not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)
echo ✓ Docker running

echo.
echo [2/3] Starting STEAM Hub services...
docker-compose up -d

echo.
echo [3/3] Opening application...
timeout /t 10 /nobreak >nul
start http://localhost:3000

echo.
echo ========================================
echo ✓ STEAM Hub Started!
echo ========================================
echo.
echo Access at: http://localhost:3000
echo.
echo Features:
echo - 1000 STEAM Lessons (Sinhala + English)
echo - FREE Voice Reading
echo - Ages 5-18
echo - Progress Tracking
echo - Quizzes and Certificates
echo.
echo To STOP: Run STOP_STEAM_HUB.bat
echo.
pause
