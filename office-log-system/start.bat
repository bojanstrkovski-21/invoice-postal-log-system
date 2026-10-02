@echo off
title Office Log System
cd /d "%~dp0"
echo Installing dependencies...
pip install -r requirements.txt -q
echo.
echo Starting server at http://localhost:5000
echo Press Ctrl+C to stop.
echo.
start /B cmd /C "timeout /t 10 /nobreak > nul & start http://localhost:5000"
python app.py
pause
