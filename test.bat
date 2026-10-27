@echo off
cd /d "%~dp0"
set "LOG=%~dp0test_log.txt"
echo ==== emuziek tests %date% %time% > "%LOG%"
echo [1/2] Backend tests (pytest)...
venv\Scripts\python.exe -m pytest tests -v -p no:cacheprovider >> "%LOG%" 2>&1
set "BACK=%errorlevel%"
echo BACKEND_EXIT %BACK% >> "%LOG%"
echo [2/2] Frontend tests (jest)...
pushd frontend
set CI=true
call npx react-scripts test --watchAll=false >> "%LOG%" 2>&1
set "FRONT=%errorlevel%"
popd
echo FRONTEND_EXIT %FRONT% >> "%LOG%"
findstr /R /C:" passed" /C:" failed" /C:"Tests:" "%LOG%"
if "%BACK%%FRONT%"=="00" ( echo TESTS_PASSED >> "%LOG%" & echo. & echo ALL TESTS PASSED ) else ( echo TESTS_FAILED >> "%LOG%" & echo. & echo SOME TESTS FAILED - see test_log.txt )
timeout /t 30
