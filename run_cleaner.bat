@echo off
REM Free Cursor & Windsurf Data Cleaner - Windows Batch Script
REM This script provides an easy way to run the cleaner on Windows

title Free Cursor ^& Windsurf Data Cleaner

echo.
echo ========================================
echo  Free Cursor ^& Windsurf Data Cleaner
echo ========================================
echo.
echo This tool will help you clean application data
echo to allow unlimited logins with different accounts.
echo.
echo IMPORTANT: Close Cursor and Windsurf before proceeding!
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    echo.
    pause
    exit /b 1
)

REM Check if the cleaner script exists
if not exist "cursor_windsurf_cleaner.py" (
    if not exist "advanced_cleaner.py" (
        echo ERROR: Cleaner script not found
        echo Please ensure cursor_windsurf_cleaner.py or advanced_cleaner.py is in the same directory
        echo.
        pause
        exit /b 1
    )
)

echo Select cleaner version:
echo 1. Basic Cleaner (cursor_windsurf_cleaner.py)
echo 2. Advanced Cleaner (advanced_cleaner.py)
echo 3. Discovery Mode (find applications only)
echo 4. Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo Running Basic Cleaner...
    python cursor_windsurf_cleaner.py
) else if "%choice%"=="2" (
    echo.
    echo Running Advanced Cleaner...
    python advanced_cleaner.py
) else if "%choice%"=="3" (
    echo.
    echo Running Discovery Mode...
    if exist "advanced_cleaner.py" (
        python advanced_cleaner.py --discover
    ) else (
        echo Discovery mode requires advanced_cleaner.py
    )
) else if "%choice%"=="4" (
    echo Exiting...
    exit /b 0
) else (
    echo Invalid choice. Please run the script again.
)

echo.
echo Script completed. Check the log files for details.
echo Backups are saved in your home directory under CursorWindsurf_*_Backups
echo.
pause
