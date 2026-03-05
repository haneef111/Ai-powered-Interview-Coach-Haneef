# Fix: Speech and Facial Scores Showing 0

## 🔴 Problem:
- Gemini content score: ✅ Working (55)
- Speech score: ❌ Shows 0
- Facial score: ❌ Shows 0

## 🎯 Root Cause:

**FFmpeg is missing!** Whisper (speech analysis) REQUIRES FFmpeg to extract audio from video files. Without it:
- Speech analysis fails → returns 0
- Facial analysis may also fail → returns 0
- Only Gemini works (doesn't need video processing)

## ✅ SOLUTION (5 Minutes):

### Step 1: Check if FFmpeg is Installed
```bash
check_ffmpeg.bat
```

OR manually:
```bash
ffmpeg -version
```

If you see version info → FFmpeg is installed ✅
If you see "not recognized" → FFmpeg is missing ❌

### Step 2: Install FFmpeg

**EASIEST - Using Chocolatey:**
```bash
choco install ffmpeg
```

**ALTERNATIVE - Manual Installation:**
1. Download: https://www.gyan.dev/ffmpeg/builds/
2. Get "ffmpeg-release-essentials.zip"
3. Extract to `C:\ffmpeg`
4. Add to PATH:
   - Windows Search → "Environment Variables"
   - System variables → "Path" → Edit
   - New → `C:\ffmpeg\bin`
   - OK → OK → OK
5. **CLOSE and REOPEN** your terminal/IDE
6. Verify: `ffmpeg -version`

**ALTERNATIVE - Using winget:**
```bash
winget install ffmpeg
```

### Step 3: Fix Python Dependencies
```bash
fix_dependencies.bat
```

This installs:
- ffmpeg-python (Python wrapper)
- Correct MediaPipe version
- Latest Gemini AI package

### Step 4: Restart Backend
```bash
python backend/app.py
```

### Step 5: Test
1. Login to application
2. Start new interview
3. Answer ONE question (10-15 seconds)
4. Complete interview
5. Check feedback

**Expected Result:**
- Speech Score: 70-85 ✅
- Facial Score: 70-80 ✅
- Content Score: 60-90 ✅
- Overall Score: Average of all three ✅

## 🔍 Verify It's Working:

### Check Backend Logs:
You should see:
```
Analyzing answer 1/10 for question 1
File exists, size: 245678 bytes
Loading Whisper model...
Transcribing audio...
Speech analysis complete - Score: 82
Facial analysis complete - Confidence: 76
Question 1 scores - Speech: 82, Facial: 76, Content: 85, Overall: 81.5
```

### If You See This → It's BROKEN:
```
Speech analysis error: ...
Facial analysis error: ...
Question 1 scores - Speech: 0, Facial: 0, Content: 85, Overall: 28.3
```

## 🚨 Still Getting 0 Scores?

### Diagnostic Steps:

1. **Run full diagnostic:**
```bash
python test_analysis_services.py
```

2. **Check video codec support:**
```bash
python check_video_support.py
```

3. **Check uploads folder:**
```bash
dir backend\uploads
```
Are there video files? If not, videos aren't being saved.

4. **Check backend logs:**
Look for these errors:
- "Video file not found" → File path issue
- "Could not open video" → Codec issue
- "Whisper error" → FFmpeg missing
- "MediaPipe error" → Package issue

### Common Issues:

**Issue:** "ffmpeg not recognized"
**Fix:** FFmpeg not in PATH. Restart terminal after installation.

**Issue:** "Could not open video file"
**Fix:** 
- Install FFmpeg
- Check if VP8/VP9 codecs are supported
- Try: `pip install opencv-python-headless`

**Issue:** "No video files in uploads"
**Fix:**
- Check browser console (F12) for upload errors
- Verify backend is receiving files
- Check file permissions on uploads folder

**Issue:** "Transcript too short or empty"
**Fix:**
- Speak louder during recording
- Check microphone is working
- Record for at least 10 seconds
- Ensure video has audio track

## 🎬 Alternative: Use MP4 Instead of WebM

If WebM continues to cause issues, change recording format:

**Edit:** `frontend/js/interview-new.js`

Find:
```javascript
const options = { mimeType: 'video/webm;codecs=vp9' };
```

Change to:
```javascript
const options = { mimeType: 'video/mp4' };
```

**Note:** Not all browsers support MP4 recording. Chrome/Edge work best with WebM.

## 📊 Expected Scores:

When working correctly:
- **Speech Score:** 60-90 (based on clarity, pace, filler words)
- **Facial Score:** 60-85 (based on eye contact, expressions)
- **Content Score:** 50-95 (based on Gemini AI evaluation)
- **Overall Score:** Weighted average (Content 40%, Speech 30%, Facial 30%)

## ✅ Success Checklist:

- [ ] FFmpeg installed (`ffmpeg -version` works)
- [ ] Dependencies installed (`fix_dependencies.bat` completed)
- [ ] Backend running without errors
- [ ] Completed one test interview
- [ ] Backend logs show "Speech analysis complete - Score: XX"
- [ ] Backend logs show "Facial analysis complete - Confidence: XX"
- [ ] Feedback page shows non-zero scores
- [ ] Overall score is calculated correctly

## 🎯 Bottom Line:

**The #1 reason for 0 scores is missing FFmpeg.**

Install FFmpeg → Restart terminal → Run fix_dependencies.bat → Restart backend → Test

That's it!

---

## 📞 Quick Commands:

```bash
# Check FFmpeg
check_ffmpeg.bat

# Fix dependencies
fix_dependencies.bat

# Test analysis
python test_analysis_services.py

# Start application
START_APPLICATION.bat
```

---

**After fixing, your scores should be accurate and non-zero!** 🎉
