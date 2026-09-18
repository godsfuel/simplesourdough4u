@echo off
TITLE Simple Sourdough 4 U - Production Server
echo Starting Simple Sourdough 4 U Production Environment...

:: Navigate to the project directory just in case it's launched from elsewhere
cd /d "%~dp0"

echo Launching Waitress WSGI Production Server...
python app.py

pause