@echo off
cd /d "%~dp0"
echo Starting SharpSplat...
.venv\Scripts\python src\sharpsplat\app.py %*
if errorlevel 1 pause
