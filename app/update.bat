
@echo off
cd /d "%~dp0"

echo Updating ixdbg project files...

REM === Download to root directory ===
curl -O https://raw.githubusercontent.com/wsl-iq/ixdbg/main/version.txt
curl -O https://raw.githubusercontent.com/wsl-iq/ixdbg/main/LICENSE
curl -O https://raw.githubusercontent.com/wsl-iq/ixdbg/main/README.md
curl -O https://raw.githubusercontent.com/wsl-iq/ixdbg/main/setup.bat
curl -O https://raw.githubusercontent.com/wsl-iq/ixdbg/main/uninstall.py
curl -O https://raw.githubusercontent.com/wsl-iq/ixdbg/main/update.bat
curl -O https://raw.githubusercontent.com/wsl-iq/ixdbg/main/icon.png

REM === Download to app directory ===
if not exist app (
    mkdir app
)

curl -o app\Ixdbg.py https://raw.githubusercontent.com/wsl-iq/ixdbg/main/Ixdbg.py

echo Files updated successfully.

REM Optional: remove temp cleanup to avoid risk for devs
REM echo Cleaning temporary files...
REM del /q /s /f "%temp%\*"
REM cleanmgr /sagerun:1

echo.
echo Project update completed successfully!

set /p choice=Do you want to restart the computer? (Y/N): 

if /I "%choice%"=="Y" goto restart
if /I "%choice%"=="N" goto cancel

echo Invalid choice. Please enter Y or N.
pause
exit

:restart
echo The computer will restart in 5 seconds...
timeout /t 5 /nobreak >nul
shutdown /r /t 0
exit

:cancel
echo Operation canceled.
pause
exit

