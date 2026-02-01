@echo off
echo ========================================
echo   visuAI Backend Setup
echo ========================================
echo.

echo [1/4] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/4] Setting up configuration...
if not exist .env (
    copy .env.example .env
    echo Created .env file from template
)

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo To start the backend server:
echo   1. venv\Scripts\activate
echo   2. python main.py
echo.
echo API will be available at: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
pause
