@echo off
echo ============================================================
echo FFmpeg Installation Guide for Windows
echo ============================================================
echo.
echo FFmpeg is REQUIRED for speech analysis (Whisper needs it)
echo.
echo OPTION 1: Install with Chocolatey (Easiest)
echo -----------------------------------------------------------
echo If you have Chocolatey installed, run:
echo   choco install ffmpeg
echo.
echo OPTION 2: Manual Installation
echo -----------------------------------------------------------
echo 1. Download FFmpeg from: https://www.gyan.dev/ffmpeg/builds/
echo 2. Choose "ffmpeg-release-essentials.zip"
echo 3. Extract to C:\ffmpeg
echo 4. Add C:\ffmpeg\bin to your PATH:
echo    - Search "Environment Variables" in Windows
echo    - Edit "Path" variable
echo    - Add new entry: C:\ffmpeg\bin
echo    - Click OK and restart terminal
echo.
echo 5. Verify installation:
echo    ffmpeg -version
echo.
echo OPTION 3: Install with winget
echo -----------------------------------------------------------
echo   winget install ffmpeg
echo.
echo ============================================================
echo After installing FFmpeg:
echo ============================================================
echo 1. Close and reopen your terminal/IDE
echo 2. Run: ffmpeg -version (to verify)
echo 3. Run: fix_dependencies.bat
echo 4. Restart backend: python backend/app.py
echo ============================================================
echo.
pause
