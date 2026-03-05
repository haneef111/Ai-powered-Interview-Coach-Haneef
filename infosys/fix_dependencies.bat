@echo off
echo ============================================================
echo Fixing Dependencies for AI Interview Coach
echo ============================================================
echo.

echo Checking FFmpeg installation...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] FFmpeg is NOT installed!
    echo FFmpeg is REQUIRED for speech analysis to work.
    echo.
    echo Please install FFmpeg first:
    echo   - Run: install_ffmpeg_guide.bat
    echo   - Or install manually from: https://www.gyan.dev/ffmpeg/builds/
    echo.
    echo After installing FFmpeg, run this script again.
    echo.
    pause
    exit /b 1
) else (
    echo [OK] FFmpeg is installed
)

echo.
cd backend

echo 1. Uninstalling old mediapipe...
pip uninstall mediapipe -y

echo.
echo 2. Installing correct mediapipe version...
pip install mediapipe==0.10.9

echo.
echo 3. Installing/Updating Google Gemini AI...
pip install --upgrade google-generativeai

echo.
echo 4. Installing ffmpeg-python...
pip install ffmpeg-python

echo.
echo 5. Verifying installations...
python -c "import mediapipe; print('MediaPipe version:', mediapipe.__version__)"
python -c "import google.generativeai as genai; print('Gemini AI: OK')"
python -c "import whisper; print('Whisper: OK')"
python -c "import cv2; print('OpenCV version:', cv2.__version__)"

echo.
echo ========================================
echo All dependencies fixed!
echo ========================================
echo.
echo Next steps:
echo 1. Restart your backend: python app.py
echo 2. Test with: python test_analysis_services.py
echo.
pause
