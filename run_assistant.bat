@echo off
echo 🚀 Starting Gwen Voice Assistant...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo ❌ .env file not found
    echo Please copy .env.example to .env and configure your API keys
    echo.
    echo Opening setup instructions...
    start SETUP_INSTRUCTIONS.md
    pause
    exit /b 1
)

REM Check if requirements are installed
python -c "import pvporcupine" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install packages
        echo Please check your internet connection and try again
        pause
        exit /b 1
    )
)

REM Start the assistant
echo ✅ All checks passed, starting assistant...
echo.
python main.pyw

REM If we get here, the assistant has stopped
echo.
echo 👋 Assistant stopped
pause