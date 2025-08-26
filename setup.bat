@echo off
echo ==========================
echo Employee Manager Installer
echo ==========================

:: --- Check Python ---
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python not found. Downloading and installing...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.12.5/python-3.12.5-amd64.exe -OutFile python_installer.exe"
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
) ELSE (
    echo Python is already installed.
)

:: --- Check MySQL ---
where mysql >nul 2>&1
IF ERRORLEVEL 1 (
    echo MySQL not found. Please install MySQL manually from https://dev.mysql.com/downloads/installer/
    pause
    exit /b
) ELSE (
    echo MySQL is already installed.
)

:: --- Create virtual environment ---
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists.
)

:: --- Activate venv ---
call venv\Scripts\activate

:: --- Install requirements ---
echo Installing Python dependencies inside virtual environment...
pip install --upgrade pip
pip install -r requirements.txt

:: --- Final Status ---
echo ==========================
echo All requirements installed in venv!
echo ==========================

:: Run main script inside venv
python main.py
pause
