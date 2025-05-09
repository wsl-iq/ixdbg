@echo off
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if %errorlevel% neq 0 (
    echo Requesting Administrator Privileges
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

python -m pip install --upgrade pip

pip install lief pefile capstone pyqt5

echo.
echo Install Successfully
pause
