@echo off
echo ========================================
echo   AI Interview Coach - Starting...
echo ========================================
echo.

echo Checking FFmpeg installation...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] FFmpeg is NOT installed!
    echo.
    echo FFmpeg is REQUIRED for speech analysis to work.
    echo Without it, speech and facial scores will be 0.
    echo.
    echo Please install FFmpeg first:
    echo   1. Run: check_ffmpeg.bat
    echo   2. Or: choco install ffmpeg
    echo   3. Then run this script again
    echo.
    echo Press any key to continue anyway (not recommended)...
    pause
) else (
    echo [OK] FFmpeg is installed
)

echo.
echo Step 1: Starting Backend Server...
echo.
start "Backend Server" cmd /k "cd backend && python app.py"

echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo.
echo Step 2: Starting Frontend Server...
echo.
start "Frontend Server" cmd /k "cd frontend && python -m http.server 8000"

echo.
echo ========================================
echo   Application Started Successfully!
echo ========================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:8000
echo.
echo Opening browser in 3 seconds...
timeout /t 3 /nobreak > nul

start http://localhost:8000

echo.
echo Both servers are running in separate windows.
echo Close those windows to stop the servers.
echo.
echo If you get zero scores for speech/facial analysis:
echo   1. Install FFmpeg: check_ffmpeg.bat
echo   2. Fix dependencies: fix_dependencies.bat
echo   3. Restart backend
echo.
pause
