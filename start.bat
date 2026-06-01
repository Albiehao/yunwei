@echo off

echo ========================================
echo   XunTian Ops Platform - Quick Start
echo ========================================
echo.

echo Step 1/4: Installing backend packages...
cd /d "%~dp0backend"
C:\Users\11859\AppData\Local\Programs\Python\Python314\python.exe -m pip install -r requirements.txt -q
if errorlevel 1 (
    echo FAILED
    pause
    exit /b 1
)
echo OK
echo.

echo Step 2/4: Installing frontend packages...
cd /d "%~dp0"
call pnpm install >nul
if errorlevel 1 (
    echo FAILED
    pause
    exit /b 1
)
echo OK
echo.

echo Step 3/4: Building frontend...
call pnpm build >nul
if errorlevel 1 (
    echo FAILED
    pause
    exit /b 1
)
echo OK
echo.

echo Step 4/4: Starting server...
echo.
echo URL:   http://localhost:3000
echo Login: admin / admin123
echo.
echo --- Server Log ---
echo.

cd /d "%~dp0backend"
C:\Users\11859\AppData\Local\Programs\Python\Python314\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 3000 --reload

echo.
echo Server stopped.
pause
