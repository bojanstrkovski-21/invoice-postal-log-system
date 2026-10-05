@echo off
cd /d "%~dp0"
echo Starting Office Log...
start "Office Log System" python app.py
timeout /t 2 /nobreak >nul
start http://localhost:5000
