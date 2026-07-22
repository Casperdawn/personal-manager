@echo off
chcp 65001 >nul
echo Building Personal Manager...

set PROJECT_DIR=%~dp0
set BACKEND_DIR=%PROJECT_DIR%backend
set FRONTEND_DIR=%PROJECT_DIR%frontend
set DIST_DIR=%PROJECT_DIR%dist

if exist "%DIST_DIR%" rmdir /s /q "%DIST_DIR%"
mkdir "%DIST_DIR%"

echo [1/5] Building frontend...
cd "%FRONTEND_DIR%"
call npm run build
if errorlevel 1 (
    echo Error: Frontend build failed!
    pause
    exit /b 1
)

echo [2/5] Preparing static files...
if exist "%BACKEND_DIR%\static" rmdir /s /q "%BACKEND_DIR%\static"
mkdir "%BACKEND_DIR%\static"
xcopy "%FRONTEND_DIR%\dist\*" "%BACKEND_DIR%\static\" /E /Y >nul

echo [3/5] Installing backend dependencies...
cd "%BACKEND_DIR%"
if not exist "venv" (
    python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Backend dependencies installation failed!
    pause
    exit /b 1
)

echo [4/5] Initializing database...
if exist "personal_manager.db" del "personal_manager.db"
python init_sample_data.py
if errorlevel 1 (
    echo Error: Database initialization failed!
    pause
    exit /b 1
)

echo [5/5] Starting server...
echo Server is starting...
echo Open your browser and visit: http://localhost:8000
echo Default account: hzs / 123
python main.py
