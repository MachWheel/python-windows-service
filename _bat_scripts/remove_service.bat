@echo off
:: Self-Elevating Batch Script
:: ----------------------------------------
:: 1. Checks if it has admin rights
:: 2. If not, relaunches itself with "Run as Administrator"
:: 3. Once elevated, stops and removes the service
:: ----------------------------------------

:: --- Check for Admin privileges ---
:: The "net session" or "net file" command returns an error if not admin.
net session >nul 2>&1
if %errorlevel%==0 (
    echo Running with administrator privileges.
) else (
    echo.
    echo ======================================================
    echo  This script needs to run as Administrator!
    echo  Attempting to elevate privileges now...
    echo ======================================================
    echo.

    :: Relaunch this batch file with admin privileges using PowerShell
    powershell.exe -Command "Start-Process -Verb runAs -FilePath '%~dp0%~nx0'"
    goto :EOF
)

:: --- At this point, we are definitely elevated. ---
echo.
echo ======================================================
echo  We are elevated. Continuing with service commands...
echo ======================================================
echo.

:: Ensure we run commands from the script's directory
cd /d "%~dp0"

:: Actual service commands
call .\my-service.exe stop
call .\my-service.exe remove

pause
