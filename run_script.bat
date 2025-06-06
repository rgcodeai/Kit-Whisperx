@echo off
setlocal

rem Activate virtual environment
call venv\Scripts\activate.bat

rem Check if virtual environment was activated
if %errorlevel% neq 0 (
    echo ERROR: Could not activate virtual environment.
    echo Please verify that 'venv' folder exists.
    echo.
    pause
    exit /b 1
)

echo ========================================
echo Virtual environment activated.
echo ========================================

echo.
echo To stop: Ctrl+C
echo.

echo ========================================
echo Starting server. Please wait...
echo ========================================
echo.

rem Run Gradio application
python app.py

rem Message when server is closed
echo.
echo Server stopped.
echo.
pause
