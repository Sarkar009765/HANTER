@echo off
echo Starting BRO-AI development environment...
echo.

:: Start Python backend
start "BRO-AI Backend" cmd /c "cd /d "%~dp0..\core" && call venv\Scripts\activate.bat && python main.py"

:: Wait for backend to start
timeout /t 3 /nobreak >nul

:: Start frontend
start "BRO-AI Frontend" cmd /c "cd /d "%~dp0..\apps\desktop" && npm run tauri-dev"

echo.
echo Backend starting on http://localhost:8000
echo Frontend starting in Tauri window
echo Close both windows to stop.
pause
