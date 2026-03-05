@echo off
echo ============================================================
echo Checking FFmpeg Installation
echo ============================================================
echo.

ffmpeg -version >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] FFmpeg is installed!
    echo.
    ffmpeg -version
    echo.
    echo ============================================================
    echo FFmpeg is ready. You can now use speech analysis.
    echo ============================================================
) else (
    echo [ERROR] FFmpeg is NOT installed!
    echo.
    echo FFmpeg is REQUIRED for speech analysis to work.
    echo Without it, speech scores will be 0.
    echo.
    echo ============================================================
    echo Installation Options:
    echo ============================================================
    echo.
    echo OPTION 1 - Chocolatey (Easiest):
    echo   choco install ffmpeg
    echo.
    echo OPTION 2 - Manual:
    echo   1. Download: https://www.gyan.dev/ffmpeg/builds/
    echo   2. Extract to C:\ffmpeg
    echo   3. Add C:\ffmpeg\bin to PATH
    echo   4. Restart terminal
    echo.
    echo OPTION 3 - winget:
    echo   winget install ffmpeg
    echo.
    echo ============================================================
    echo After installation, run this script again to verify.
    echo ============================================================
)

echo.
pause
