@echo off
echo Setting up BRO-AI development environment...
echo.

:: Check Python
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python not found. Please install Python 3.11+
    exit /b 1
)

:: Create virtual environment
cd /d "%~dp0..\core"
if not exist "venv" (
    python -m venv venv
    echo Created Python virtual environment
)

:: Activate and install dependencies
call venv\Scripts\activate.bat
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Warning: Some Python packages failed to install
)

:: Install frontend dependencies
cd /d "%~dp0..\apps\desktop"
if exist "package.json" (
    call npm install
    echo Frontend dependencies installed
)

:: Create data directory
if not exist "%~dp0..\data" mkdir "%~dp0..\data"

echo.
echo Setup complete! Run scripts\dev.bat to start development.
pause
