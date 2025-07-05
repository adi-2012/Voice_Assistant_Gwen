@echo off
REM Advanced Gwen Assistant Startup Script
REM Features: Error handling, logging, auto-restart, dependency checking

setlocal enabledelayedexpansion

REM Configuration
set GWEN_DIR=C:\Gwen
set PYTHON_EXE=C:\Program Files\Python313\pythonw.exe
set PYTHON_VISIBLE=C:\Program Files\Python313\python.exe
set MAIN_FILE=main.pyw
set LOG_FILE=gwen_startup.log
set MAX_RESTARTS=3
set RESTART_COUNT=0

REM Create log entry
echo [%date% %time%] Starting Gwen Assistant >> "%GWEN_DIR%\%LOG_FILE%"

REM Check if Gwen directory exists
if not exist "%GWEN_DIR%" (
    echo ERROR: Gwen directory not found: %GWEN_DIR%
    echo [%date% %time%] ERROR: Gwen directory not found >> "%GWEN_DIR%\%LOG_FILE%"
    pause
    exit /b 1
)

REM Change to Gwen directory
cd /d "%GWEN_DIR%"

REM Check if Python exists
if not exist "%PYTHON_EXE%" (
    echo ERROR: Python not found at: %PYTHON_EXE%
    echo [%date% %time%] ERROR: Python not found >> "%LOG_FILE%"
    pause
    exit /b 1
)

REM Check if main.pyw exists
if not exist "%MAIN_FILE%" (
    echo ERROR: Main file not found: %MAIN_FILE%
    echo [%date% %time%] ERROR: Main file not found >> "%LOG_FILE%"
    pause
    exit /b 1
)

REM Check if wake word file exists
if not exist "hey-Gwen_en_windows_v3_0_0.ppn" (
    echo WARNING: Wake word file not found!
    echo [%date% %time%] WARNING: Wake word file not found >> "%LOG_FILE%"
)

echo Gwen Assistant is starting in background...
echo Check system tray or Task Manager for pythonw.exe process
echo [%date% %time%] Gwen started successfully >> "%LOG_FILE%"

:start_loop
REM Start Gwen (hidden mode)
"%PYTHON_EXE%" "%MAIN_FILE%"

REM If we get here, Gwen exited
set /a RESTART_COUNT+=1
echo [%date% %time%] Gwen exited, restart attempt %RESTART_COUNT% >> "%LOG_FILE%"

if %RESTART_COUNT% LSS %MAX_RESTARTS% (
    echo Restarting Gwen... (Attempt %RESTART_COUNT%/%MAX_RESTARTS%)
    timeout /t 5 /nobreak >nul
    goto start_loop
) else (
    echo Maximum restart attempts reached. Stopping.
    echo [%date% %time%] Maximum restart attempts reached >> "%LOG_FILE%"
)

echo Gwen Assistant stopped.
pause