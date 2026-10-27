@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set "ROOT=%~dp0"
set "LOG=%ROOT%setup_log.txt"
echo ==== emuziek setup %date% %time% > "%LOG%"
echo Setting up emuziek (first run takes 10-20 minutes). Log: setup_log.txt

echo [1/5] Checking model and dataset files...
if not exist "backend\models\emotion_cnn.h5" ( echo MODEL_MISSING >> "%LOG%" & echo backend\models\emotion_cnn.h5 is missing - re-download the repo & goto :fail )
if not exist "backend\data\data.csv" ( echo DATA_MISSING >> "%LOG%" & echo backend\data\data.csv is missing - re-download the repo & goto :fail )
echo FILES_OK >> "%LOG%"

echo [2/5] Finding Python 3.10-3.12...
set "PY="
for %%v in (3.12 3.11 3.10) do (
  if not defined PY (
    py -%%v -c "import sys" >nul 2>&1
    if !errorlevel!==0 set "PY=py -%%v"
  )
)
if not defined PY ( echo NO_PYTHON_3.10-3.12 >> "%LOG%" & echo Please install Python 3.12 from python.org & goto :fail )
echo using !PY! >> "%LOG%"

echo [3/5] Creating virtual environment (venv)...
if not exist "venv\Scripts\python.exe" !PY! -m venv venv >> "%LOG%" 2>&1
if not exist "venv\Scripts\python.exe" ( echo VENV_FAILED >> "%LOG%" & goto :fail )

echo [4/5] Installing Python packages...
venv\Scripts\python.exe -m pip install --upgrade pip >> "%LOG%" 2>&1
venv\Scripts\python.exe -m pip install -r backend\requirements.txt >> "%LOG%" 2>&1
if !errorlevel! neq 0 ( echo PIP_FAILED >> "%LOG%" & goto :fail )
echo PIP_OK >> "%LOG%"

echo [5/5] Installing and building the React frontend...
where npm >nul 2>&1
if !errorlevel! neq 0 ( echo NO_NODE >> "%LOG%" & echo Please install Node.js from nodejs.org & goto :fail )
pushd frontend
call npm install --no-audit --no-fund >> "%LOG%" 2>&1
if !errorlevel! neq 0 ( popd & echo NPM_INSTALL_FAILED >> "%LOG%" & goto :fail )
call npm run build >> "%LOG%" 2>&1
if !errorlevel! neq 0 ( popd & echo NPM_BUILD_FAILED >> "%LOG%" & goto :fail )
popd
echo NPM_OK >> "%LOG%"

if not exist "backend\.env" copy "backend\.env.example" "backend\.env" >nul

echo SETUP_DONE >> "%LOG%"
echo.
echo Setup complete!  Next: add Spotify keys to backend\.env (optional), then double-click run.bat
timeout /t 20
exit /b 0

:fail
echo SETUP_FAILED >> "%LOG%"
echo Setup failed - see setup_log.txt
timeout /t 60
exit /b 1
