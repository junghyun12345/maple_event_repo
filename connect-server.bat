@echo off
title Maple Event Server (43.200.15.23)
echo Connecting to Maple Event server...
ssh -i "%USERPROFILE%\Downloads\maplelistprojkey.pem" ubuntu@43.200.15.23
echo.
echo (session closed - press any key to close this window)
pause >nul
