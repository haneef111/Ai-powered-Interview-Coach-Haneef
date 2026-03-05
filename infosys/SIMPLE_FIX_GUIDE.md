# Simple Fix Guide - Zero Scores Issue

## 🎯 The Problem

You're getting:
- Content Score: 55 ✅
- Speech Score: 0 ❌
- Facial Score: 0 ❌

## 🎯 The Cause

**FFmpeg is not installed.** Whisper needs FFmpeg to extract audio from your video recordings.

## 🎯 The Fix (5 Minutes)

### 1. Open Command Prompt

### 2. Check FFmpeg:
```bash
ffmpeg -version
```

**If you see version info** → FFmpeg is installed, skip to step 4
**If you see "not recognized"** → FFmpeg is missing, continue to step 3

### 3. Install FFmpeg:

**Easiest way (if you have Chocolatey):**
```bash
choco install ffmpeg
```

**Alternative (if you have winget):**
```bash
winget install ffmpeg
```

**Manual installation:**
1. Go to: https://www.gyan.dev/ffmpeg/builds/
2. Download "ffmpeg-release-essentials.zip"
3. Extract to `C:\ffmpeg`
4. Add to PATH:
   - Press Windows key
   - Type "environment variables"
   - Click "Edit system environment variables"
   - Click "Environment Variables" button
   - Under "System variables", find "Path"
   - Click "Edit"
   - Click "New"
   - Type: `C:\ffmpeg\bin`
   - Click OK on all windows
5. **Close and reopen your Command Prompt**

### 4. Verify FFmpeg:
```bash
ffmpeg -version
```
You should see version information.

### 5. Fix Python Dependencies:
```bash
fix_dependencies.bat
```

Wait for it to complete.

### 6. Restart Backend:
```bash
python backend/app.py
```

### 7. Test:
1. Open http://localhost:8000
2. Login
3. Start new interview
4. Answer ONE question (speak for 10-15 seconds)
5. Complete interview
6. Check feedback

**Expected:**
- Speech Score: 70-85 ✅
- Facial Score: 70-80 ✅
- Content Score: 60-90 ✅

---

## ✅ How to Know It Worked

### In Backend Logs:
```
Speech analysis complete - Score: 82
Facial analysis complete - Confidence: 76
Question 1 scores - Speech: 82, Facial: 76, Content: 85
```

### In Feedback Page:
- All three scores are non-zero
- Overall score is calculated correctly
- You see detailed analysis for each question

---

## 🆘 Still Not Working?

### Run Full Diagnostics:
```bash
run_all_diagnostics.bat
```

This will check everything and tell you exactly what's wrong.

### Or Read Detailed Guides:
- `TROUBLESHOOTING_ZERO_SCORES.md` - Comprehensive troubleshooting
- `UNDERSTANDING_ZERO_SCORES.md` - Technical explanation
- `FIX_ERRORS_GUIDE.md` - Common errors

---

## 📞 Quick Commands

```bash
# Check
check_ffmpeg.bat                  # Is FFmpeg installed?

# Fix
fix_dependencies.bat              # Fix packages

# Diagnose
python diagnose_zero_scores.py    # What's wrong?

# Run
START_APPLICATION.bat             # Start app
```

---

## 🎉 That's It!

**Most users fix this in 5 minutes by installing FFmpeg.**

1. Install FFmpeg
2. Run fix_dependencies.bat
3. Restart backend
4. Test

Done! 🚀
