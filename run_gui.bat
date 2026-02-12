@echo off
setlocal

set "PROJECT_DIR=%~dp0"
if "%PROJECT_DIR:~-1%"=="\" set "PROJECT_DIR=%PROJECT_DIR:~0,-1%"
set "VENV_PY=%PROJECT_DIR%\.venv\Scripts\python.exe"

if not exist "%VENV_PY%" (
    echo Virtual environment not found. Running installer first...
    echo.
    call "%PROJECT_DIR%\install.bat"
    if not exist "%VENV_PY%" exit /b 1
)

start "" "%VENV_PY%" "%PROJECT_DIR%\gui.py"
