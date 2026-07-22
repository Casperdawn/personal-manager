@echo off
echo 开始构建 Personal Manager...

set PROJECT_DIR=%~dp0
set BACKEND_DIR=%PROJECT_DIR%backend
set FRONTEND_DIR=%PROJECT_DIR%frontend
set DIST_DIR=%PROJECT_DIR%dist

if exist "%DIST_DIR%" rmdir /s /q "%DIST_DIR%"
mkdir "%DIST_DIR%"

echo 1. 构建前端...
cd "%FRONTEND_DIR%"
call npm run build
if errorlevel 1 (
    echo 前端构建失败！
    pause
    exit /b 1
)

echo 2. 准备静态文件...
if exist "%BACKEND_DIR%\static" rmdir /s /q "%BACKEND_DIR%\static"
mkdir "%BACKEND_DIR%\static"
xcopy "%FRONTEND_DIR%\dist\*" "%BACKEND_DIR%\static\" /E /Y

echo 3. 安装后端依赖...
cd "%BACKEND_DIR%"
if not exist "venv" (
    python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt
if errorlevel 1 (
    echo 后端依赖安装失败！
    pause
    exit /b 1
)

echo 4. 初始化数据库...
if exist "personal_manager.db" del "personal_manager.db"
python init_sample_data.py
if errorlevel 1 (
    echo 数据库初始化失败！
    pause
    exit /b 1
)

echo 5. 启动服务...
echo 服务即将启动，请在浏览器中访问 http://localhost:8000
echo 默认账号: hzs / 123
python main.py
