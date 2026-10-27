@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"
if not exist "venv\Scripts\python.exe" ( echo Run setup.bat first. & timeout /t 10 & exit /b 1 )
start "emuziek backend - Flask :5000" /D "%~dp0backend" cmd /k ""%~dp0venv\Scripts\python.exe" app.py"

rem Loading TensorFlow and the model takes a while: wait for the backend before opening the app
echo Waiting for the backend to start (can take up to a minute)...
set /a TRIES=0
:wait
curl -s -o nul http://127.0.0.1:5000/api/health && goto :ready
set /a TRIES+=1
if !TRIES! geq 90 (
  echo The backend did not start - check the "emuziek backend" window for the error.
  timeout /t 30
  exit /b 1
)
timeout /t 2 /nobreak >nul
goto :wait

:ready
echo Backend is ready. Starting the React app...
start "emuziek frontend - React :3000" /D "%~dp0frontend" cmd /k "npm start"
