@echo off
rem Setup script for WhisperX CPU-only environment
rem This script creates a virtual environment and installs all dependencies from requirements_cpu.txt

echo ========================================
echo WhisperX CPU Environment Setup
echo ========================================
echo.

rem Create a new virtual environment for this project
echo Creating virtual environment...
python -m venv venv
rem Check if the virtual environment was created successfully
if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment.
    echo Make sure Python is installed and accessible from command line.
    goto end
)
echo Virtual environment created successfully.
echo.

rem Activate the newly created virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
rem Check if the virtual environment was activated successfully
if %errorlevel% neq 0 (
    echo Error: Failed to activate virtual environment.
    goto end
)
echo Virtual environment activated successfully.
echo.

rem Update pip to the latest version
echo Updating pip to latest version...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo Error: Failed to update pip.
    goto end
)
echo Pip updated successfully.
echo.

rem Check if requirements_cpu.txt exists
if not exist "requirements\requirements_cpu.txt" (
    echo Error: requirements_cpu.txt file not found in requirements directory.
    echo Please make sure the requirements_cpu.txt file is in the requirements folder.
    goto end
)

rem Install all dependencies from requirements_cpu.txt
echo Installing all dependencies from requirements\requirements_cpu.txt...
echo This may take several minutes, please wait...
pip install -r requirements\requirements_cpu.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies from requirements\requirements_cpu.txt.
    echo Please check the file and try again.
    goto end
)
echo.
echo All dependencies installed successfully!
echo.

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo Your WhisperX CPU environment is ready to use.
echo.


:end
rem Label to jump to if there is an error in any of the previous operations or when finishing the script
echo Press any key to close this window...
pause > nul
