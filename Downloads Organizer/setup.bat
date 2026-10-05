@echo off
title Installing Downloads Organizer Dependencies...
echo ==================================================
echo   Installing required Python packages for Organizer
echo ==================================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python was not found on your system PATH!
    echo Please make sure Python is installed and added to PATH.
    echo.
    pause
    exit /b
)

echo Python detected. Installing required libraries...
echo.

python -m pip install -r requirements.txt

echo.
echo ==================================================
echo   All dependencies installed successfully!
echo ==================================================
echo.

echo Adding Downloads Organizer to Windows Startup...
set "target=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\DownloadsOrganizer.lnk"
set "script=%~dp0downloads_organizer.pyw"

powershell -Command "New-Item -ItemType SymbolicLink -Path '%target%' -Value '%script%' -Force" >nul 2>&1

if %errorlevel% neq 0 (
    powershell -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut('%target%');$s.TargetPath='%script%';$s.WorkingDirectory='%~dp0';$s.Save()"
)

echo Success! The organizer will now run silently whenever you log in.
pause