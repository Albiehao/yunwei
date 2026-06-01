@echo off
chcp 65001 >nul
echo ========================================
echo   寻天运维平台 - 一键启动
echo ========================================
echo.

REM 构建前端
echo [1/3] 构建前端...
cd /d "%~dp0"
call pnpm build
if %errorlevel% neq 0 (
    echo 前端构建失败！
    pause
    exit /b 1
)
echo 前端构建成功！
echo.

REM 安装后端依赖
echo [2/3] 安装后端依赖...
cd backend
call pip install -r requirements.txt -q
echo 后端依赖安装完成！
echo.

REM 启动服务
echo [3/3] 启动服务...
echo.
echo 访问地址: http://localhost:3000
echo 登录账号: admin / admin123
echo.
uvicorn app.main:app --host 0.0.0.0 --port 3000 --reload
pause
