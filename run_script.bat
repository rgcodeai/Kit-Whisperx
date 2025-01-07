@echo off
rem Activates the virtual environment required for the project
echo Activating virtual environment...
call venv\Scripts\activate.bat

rem Checks if the virtual environment was activated successfully
if %errorlevel% neq 0 (
    echo Error activating virtual environment.
    goto end
)

rem Runs the Python script that performs the desired task
echo Running Python script...
python app.py

rem Checks if the Python script ran successfully
if %errorlevel% neq 0 (
    echo Error running Python script.
    goto end
)

rem Displays a success message if the Python script executed without errors
echo.
echo Script executed successfully.

:end
rem Label to jump to if there is an error in any of the previous operations or when finishing the script
echo Press any key to close...
pause > nul
