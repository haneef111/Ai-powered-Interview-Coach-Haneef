@echo off
echo ============================================================
echo RUNNING ALL DIAGNOSTICS
echo ============================================================
echo.
echo This will check everything needed for the application to work.
echo.
pause

echo.
echo ============================================================
echo [1/5] Checking FFmpeg...
echo ============================================================
call check_ffmpeg.bat

echo.
echo ============================================================
echo [2/5] Checking Video Codec Support...
echo ============================================================
python check_video_support.py

echo.
echo ============================================================
echo [3/5] Testing Analysis Services...
echo ============================================================
python test_analysis_services.py

echo.
echo ============================================================
echo [4/5] Diagnosing Zero Scores...
echo ============================================================
python diagnose_zero_scores.py

echo.
echo ============================================================
echo [5/5] Checking Interview Scores in Database...
echo ============================================================
python check_interview_scores.py

echo.
echo ============================================================
echo DIAGNOSTICS COMPLETE
echo ============================================================
echo.
echo Review the output above to identify any issues.
echo.
echo If FFmpeg is missing:
echo   1. Run: install_ffmpeg_guide.bat
echo   2. Install FFmpeg
echo   3. Run: fix_dependencies.bat
echo   4. Restart backend
echo.
echo If other issues found:
echo   - See: TROUBLESHOOTING_ZERO_SCORES.md
echo   - See: FIX_ERRORS_GUIDE.md
echo   - See: ZERO_SCORES_FIX.md
echo.
pause
