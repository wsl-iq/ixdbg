@echo off
cd /d "%~dp0"

echo Updating files...

curl -O https://raw.githubusercontent.com/wsl-iq/ixdbg/main/LICENSE
curl -O https://raw.githubusercontent.com/wsl-iq/ixdbg/main/README.md
curl -O https://raw.githubusercontent.com/wsl-iq/ixdbg/main/ixdbg.py
curl -O https://raw.githubusercontent.com/wsl-iq/ixdbg/main/setup.bat
curl -O https://raw.githubusercontent.com/wsl-iq/ixdbg/main/uninstall.py
curl -O https://raw.githubusercontent.com/wsl-iq/ixdbg/main/update.bat
curl -O https://raw.githubusercontent.com/wsl-iq/ixdbg/main/icon.png

echo Finish Update Files 

echo Cleaning temporary files...
del /q /s /f "%temp%\*"
cleanmgr /sagerun:1

echo Project update completed successfully!

set /p choice=Do you want to restart the computer? (Y/N): 

if /I "%choice%"=="Y" goto restart
if /I "%choice%"=="N" goto cancel

echo Invalid choice, please enter Y or N.
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
