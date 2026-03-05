@echo off
echo ========================================
echo   Starting Frontend Server...
echo ========================================
echo.
echo Frontend will be available at:
echo http://localhost:8000
echo.
cd frontend
python -m http.server 8000
pause
