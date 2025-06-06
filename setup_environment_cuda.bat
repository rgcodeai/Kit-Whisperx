@echo off
rem Setup script for WhisperX CUDA-enabled environment
rem This script creates a virtual environment and installs all dependencies from requirements_cuda.txt

echo ========================================
echo WhisperX CUDA Environment Setup
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

rem Check if requirements_cuda.txt exists in the requirements folder
if not exist "requirements\requirements_cuda.txt" (
    echo Error: requirements_cuda.txt file not found in requirements folder.
    echo Please make sure the requirements_cuda.txt file is in the 'requirements' folder.
    goto end
)

rem Install all dependencies from requirements_cuda.txt (without torch)
echo Installing all dependencies from requirements_cuda.txt...
echo This may take several minutes, please wait...
pip install -r requirements\requirements_cuda.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies from requirements_cuda.txt.
    echo Please check the file and try again.
    goto end
)
echo.
echo Dependencies installed successfully!
echo.

rem Install PyTorch with CUDA support
echo Installing PyTorch with CUDA support...
pip install torch==2.2.0+cu121 torchaudio==2.2.0+cu121 --index-url https://download.pytorch.org/whl/cu121
if %errorlevel% neq 0 (
    echo Error: Failed to install PyTorch with CUDA support.
    echo Make sure you have CUDA 12.1 installed on your system.
    goto end
)
echo.
echo PyTorch with CUDA installed successfully!
echo.

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo Your WhisperX CUDA environment is ready to use.
echo.

:end
rem Label to jump to if there is an error in any of the previous operations or when finishing the script
echo Press any key to close this window...
pause > nul
