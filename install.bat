@echo off
setlocal EnableDelayedExpansion
title Civico.net Scraper - Windows Installer
echo ============================================
echo   Civico.net Scraper - Setup
echo ============================================
echo.

:: ── Locate project directory (where this .bat lives) ──
set "PROJECT_DIR=%~dp0"
:: Remove trailing backslash
if "%PROJECT_DIR:~-1%"=="\" set "PROJECT_DIR=%PROJECT_DIR:~0,-1%"

set "VENV_DIR=%PROJECT_DIR%\.venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
set "VENV_PIP=%VENV_DIR%\Scripts\pip.exe"
set "REQ_FILE=%PROJECT_DIR%\requirements.txt"

:: ── Step 1: Check if Python 3.10+ is already installed ──
echo [1/4] Checking for Python...

set "PYTHON_CMD="

:: Try py launcher first (most reliable on Windows)
py -3 --version >nul 2>&1
if !errorlevel! equ 0 (
    set "PYTHON_CMD=py -3"
    goto :python_found
)

:: Try python3
python3 --version >nul 2>&1
if !errorlevel! equ 0 (
    set "PYTHON_CMD=python3"
    goto :python_found
)

:: Try python
python --version >nul 2>&1
if !errorlevel! equ 0 (
    set "PYTHON_CMD=python"
    goto :python_found
)

:: No Python found — install it
echo   Python not found. Installing...
goto :install_python

:python_found
:: Verify version is 3.10+
for /f "tokens=2 delims= " %%v in ('!PYTHON_CMD! --version 2^>^&1') do set "PY_VER=%%v"
for /f "tokens=1,2 delims=." %%a in ("!PY_VER!") do (
    set "PY_MAJOR=%%a"
    set "PY_MINOR=%%b"
)

if !PY_MAJOR! lss 3 goto :install_python
if !PY_MAJOR! equ 3 if !PY_MINOR! lss 10 goto :install_python

echo   Found Python !PY_VER! (!PYTHON_CMD!)
goto :create_venv

:: ── Step 2: Install Python via winget or manual download ──
:install_python
echo.
echo   Installing Python 3.13...

:: Try winget first (available on Windows 10 1709+ and all Windows 11)
winget --version >nul 2>&1
if !errorlevel! equ 0 (
    echo   Using winget...
    winget install Python.Python.3.13 --accept-package-agreements --accept-source-agreements
    if !errorlevel! equ 0 (
        echo.
        echo   Python installed successfully via winget.
        echo   NOTE: You may need to close and reopen this terminal for PATH changes.
        echo         Then run install.bat again.
        echo.
        :: Refresh PATH for current session
        set "PATH=%LOCALAPPDATA%\Programs\Python\Python313\;%LOCALAPPDATA%\Programs\Python\Python313\Scripts\;%PATH%"
        set "PYTHON_CMD=py -3"
        py -3 --version >nul 2>&1
        if !errorlevel! equ 0 goto :create_venv
        set "PYTHON_CMD=python"
        python --version >nul 2>&1
        if !errorlevel! equ 0 goto :create_venv
        echo   Please restart this script after reopening your terminal.
        pause
        exit /b 1
    )
)

:: Fallback: download installer from python.org
echo   winget not available. Downloading from python.org...
set "PY_INSTALLER=%TEMP%\python-3.13-installer.exe"
echo   Downloading Python 3.13 installer...
powershell -NoProfile -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.13.2/python-3.13.2-amd64.exe' -OutFile '%PY_INSTALLER%'"
if not exist "%PY_INSTALLER%" (
    echo.
    echo   ERROR: Failed to download Python installer.
    echo   Please install Python 3.13 manually from https://www.python.org/downloads/
    echo   Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo   Running installer (please follow the prompts)...
echo   IMPORTANT: Check "Add Python to PATH" at the bottom of the installer!
"%PY_INSTALLER%" InstallAllUsers=0 PrependPath=1 Include_test=0
if !errorlevel! neq 0 (
    echo   ERROR: Python installation failed or was cancelled.
    pause
    exit /b 1
)
del "%PY_INSTALLER%" >nul 2>&1

:: Refresh PATH
set "PATH=%LOCALAPPDATA%\Programs\Python\Python313\;%LOCALAPPDATA%\Programs\Python\Python313\Scripts\;%PATH%"
set "PYTHON_CMD=py -3"
py -3 --version >nul 2>&1
if !errorlevel! neq 0 (
    set "PYTHON_CMD=python"
    python --version >nul 2>&1
    if !errorlevel! neq 0 (
        echo.
        echo   ERROR: Python still not found after installation.
        echo   Please close this window, reopen a new terminal, and run install.bat again.
        pause
        exit /b 1
    )
)
echo   Python installed successfully.

:: ── Step 3: Create virtual environment ──
:create_venv
echo.
echo [2/4] Creating virtual environment...

if exist "%VENV_PY%" (
    echo   Virtual environment already exists. Updating...
) else (
    !PYTHON_CMD! -m venv "%VENV_DIR%"
    if !errorlevel! neq 0 (
        echo   ERROR: Failed to create virtual environment.
        echo   Try manually: !PYTHON_CMD! -m venv "%VENV_DIR%"
        pause
        exit /b 1
    )
    echo   Created .venv\
)

:: ── Step 4: Upgrade pip ──
echo.
echo [3/4] Upgrading pip...
"%VENV_PY%" -m pip install --upgrade pip --quiet
if !errorlevel! neq 0 (
    echo   WARNING: pip upgrade failed, continuing anyway...
)

:: ── Step 5: Install dependencies ──
echo.
echo [4/4] Installing dependencies...

if exist "%REQ_FILE%" (
    "%VENV_PIP%" install -r "%REQ_FILE%" --quiet
) else (
    echo   requirements.txt not found, installing defaults...
    "%VENV_PIP%" install requests tqdm --quiet
)
if !errorlevel! neq 0 (
    echo   ERROR: Failed to install dependencies.
    pause
    exit /b 1
)

:: ── Verify tkinter ──
echo.
echo Verifying tkinter...
"%VENV_PY%" -c "import tkinter; print('  tkinter OK')" 2>nul
if !errorlevel! neq 0 (
    echo   WARNING: tkinter not available. The GUI may not work.
    echo   tkinter is normally bundled with the Python Windows installer.
    echo   Re-install Python and ensure "tcl/tk and IDLE" is checked.
)

:: ── Done ──
echo.
echo ============================================
echo   Setup complete!
echo ============================================
echo.
echo   To launch the GUI:
echo     %VENV_DIR%\Scripts\python.exe gui.py
echo.
echo   Or simply:
echo     python gui.py
echo   (the bootstrap will find the venv automatically)
echo.
echo   To use the CLI scraper:
echo     %VENV_DIR%\Scripts\python.exe scraper.py --help
echo.
pause
