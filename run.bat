@echo off
echo 多屏幕内容管理器启动中...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python 3.6或更高版本
    pause
    exit /b 1
)

REM 检查并安装依赖
echo 检查依赖包...
pip install -r requirements.txt

REM 启动程序
echo 启动多屏幕内容管理器...
python main.py

pause