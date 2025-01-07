@echo off
rem Create a new virtual environment for this project
echo Creating virtual environment...
python -m venv venv
rem Check if the virtual environment was created successfully
if %errorlevel% neq 0 (
    echo Error creating virtual environment.
    goto end
)

rem Activate the newly created virtual environment
echo Activating virtual environment...
call venv/Scripts/activate.bat
rem Check if the virtual environment was activated successfully
if %errorlevel% neq 0 (
    echo Error activating virtual environment.
    goto end
)

rem Update pip to the latest version
echo Updating pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo Error updating pip.
    goto end
)

rem Install the specified dependencies
echo Installing dependencies...
pip install gradio==5.9.1 whisperx==3.3.0 numpy==1.24.4
if %errorlevel% neq 0 (
    echo Error installing gradio, whisperx, or numpy.
    goto end
)

rem Install torch and torchaudio with CUDA 12.1 support
echo Installing torch and torchaudio...
pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0 --index-url https://download.pytorch.org/whl/cpu
if %errorlevel% neq 0 (
    echo Error installing torch or torchaudio.
    goto end
)

rem Confirm that the environment is ready to use
echo.
echo Development environment ready.

:end
rem Label to jump to if there is an error in any of the previous operations or when finishing the script
echo Press any key to close....
pause > nul
