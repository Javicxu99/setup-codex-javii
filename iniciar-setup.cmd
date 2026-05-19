@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0iniciar-setup.ps1" %*
exit /b %ERRORLEVEL%
