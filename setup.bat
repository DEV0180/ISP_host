@echo off
REM Sleep Quality Analysis API - Windows Setup Script
REM This script automates the setup process

setlocal enabledelayedexpansion

echo.
echo ===============================================
echo Sleep Quality Analysis API - Setup
echo ===============================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found!
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo ✓ Python is installed
python --version

REM Create virtual environment
echo.
echo Creating virtual environment...
if exist venv (
    echo Virtual environment already exists
) else (
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install requirements
echo.
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    echo Try running: pip install -r requirements.txt
    pause
    exit /b 1
)
echo ✓ Dependencies installed

REM Create .env file if not exists
echo.
if exist .env (
    echo ✓ .env file already exists
) else (
    if exist .env.example (
        copy .env.example .env >nul
        echo ✓ .env file created from .env.example
    ) else (
        echo Warning: .env.example not found
    )
)

REM Check for model file
echo.
echo ✓ Checking for model file...
if exist sleep_model.h5 (
    echo ✓ Model file found: sleep_model.h5
) else (
    echo ⚠ Warning: sleep_model.h5 not found
    echo Please copy your trained model to this directory
    echo Expected location: %cd%\sleep_model.h5
)

REM Setup complete
echo.
echo ===============================================
echo ✓ Setup Complete!
echo ===============================================
echo.
echo To start the server, run:
echo   python main.py
echo.
echo Then visit in your browser:
echo   http://localhost:8000/docs
echo.
pause
