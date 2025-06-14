#!/bin/bash
# Free Cursor & Windsurf Data Cleaner - Unix/Linux/macOS Shell Script
# This script provides an easy way to run the cleaner on Unix-like systems

set -e

echo ""
echo "========================================"
echo " Free Cursor & Windsurf Data Cleaner"
echo "========================================"
echo ""
echo "This tool will help you clean application data"
echo "to allow unlimited logins with different accounts."
echo ""
echo "IMPORTANT: Close Cursor and Windsurf before proceeding!"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python is not installed or not in PATH"
        echo "Please install Python 3.7+ and try again"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "Using Python: $($PYTHON_CMD --version)"
echo ""

# Check if the cleaner script exists
if [[ ! -f "cursor_windsurf_cleaner.py" ]] && [[ ! -f "advanced_cleaner.py" ]]; then
    echo "ERROR: Cleaner script not found"
    echo "Please ensure cursor_windsurf_cleaner.py or advanced_cleaner.py is in the same directory"
    exit 1
fi

echo "Select cleaner version:"
echo "1. Basic Cleaner (cursor_windsurf_cleaner.py)"
echo "2. Advanced Cleaner (advanced_cleaner.py)"
echo "3. Discovery Mode (find applications only)"
echo "4. Exit"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        if [[ -f "cursor_windsurf_cleaner.py" ]]; then
            echo ""
            echo "Running Basic Cleaner..."
            $PYTHON_CMD cursor_windsurf_cleaner.py
        else
            echo "ERROR: cursor_windsurf_cleaner.py not found"
            exit 1
        fi
        ;;
    2)
        if [[ -f "advanced_cleaner.py" ]]; then
            echo ""
            echo "Running Advanced Cleaner..."
            $PYTHON_CMD advanced_cleaner.py
        else
            echo "ERROR: advanced_cleaner.py not found"
            exit 1
        fi
        ;;
    3)
        if [[ -f "advanced_cleaner.py" ]]; then
            echo ""
            echo "Running Discovery Mode..."
            $PYTHON_CMD advanced_cleaner.py --discover
        else
            echo "Discovery mode requires advanced_cleaner.py"
            exit 1
        fi
        ;;
    4)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "Script completed. Check the log files for details."
echo "Backups are saved in your home directory under CursorWindsurf_*_Backups"
echo ""

# Make the script pause on macOS/Linux (similar to Windows pause)
if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
    read -p "Press Enter to continue..."
fi
