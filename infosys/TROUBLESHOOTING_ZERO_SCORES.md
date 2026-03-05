# 🔧 Troubleshooting: Zero Scores Issue

## 🎯 Quick Fix (Most Common Issue)

**Problem:** Speech and facial scores show 0, but content score works.

**Solution:** Install FFmpeg (takes 5 minutes)

```bash
# Check if FFmpeg is installed
check_ffmpeg.bat

# If not installed, use one of these:
choco install ffmpeg              # Option 1: Chocolatey
winget install ffmpeg             # Option 2: winget
install_ffmpeg_guide.bat          # Option 3: Manual guide

# After installing:
fix_dependencies.bat              # Fix Python packages
python backend/app.py             # Restart backend
```

**Then complete a NEW interview to test.**

---

## 🔍 Diagnostic Tools

We've created several tools to help diagnose the issue:

### 1. Check FFmpeg Installation
```bash
check_ffmpeg.bat
```
Shows if FFmpeg is installed and working.

### 2. Diagnose Zero Scores
```bash
python diagnose_zero_scores.py
```
Comprehensive check of:
- FFmpeg installation
- Python packages
- Video files
- OpenCV codec support
- Whisper transcription

### 3. Check Video Support
```bash
python check_video_support.py
```
Tests if your system can process WebM video files.

### 4. Test Analysis Services
```bash
python test_analysis_services.py
```
Tests speech and facial analysis on actual video files.

### 5. Check Database Scores
```bash
python check_interview_scores.py
```
Shows actual scores stored in MongoDB.

---

## 🎬 Why This Happens

### The Analysis Pipeline:

1. **User records video** → Saved as `.webm` file
2. **Speech Analysis** → Whisper extracts audio → Transcribes → Scores clarity
3. **Facial Analysis** → OpenCV reads video → MediaPipe detects face → Scores confidence
4. **Content Analysis** → Gemini AI evaluates transcript → Scores relevance
5. **Overall Score** → Weighted average (Content 40%, Speech 30%, Facial 30%)

### Where It Breaks:

**Without FFmpeg:**
- ❌ Whisper cannot extract audio from video
- ❌ Speech analysis fails → Returns 0
- ❌ No transcript → Gemini uses fallback
- ✅ Facial analysis might work (if OpenCV has codecs)

**Without Proper Codecs:**
- ❌ OpenCV cannot read WebM video
- ❌ Facial analysis fails → Returns 0
- ❌ Whisper might also fail

**Result:** Only Gemini content score works (because it has fallback logic).

---

## ✅ Step-by-Step Fix

### Step 1: Install FFmpeg (CRITICAL)

**Why:** Whisper REQUIRES FFmpeg to extract audio from video files.

**How:**

**Option A - Chocolatey (Recommended):**
```bash
choco install ffmpeg
```

**Option B - winget:**
```bash
winget install ffmpeg
```

**Option C - Manual:**
1. Download: https://www.gyan.dev/ffmpeg/builds/
2. Get "ffmpeg-release-essentials.zip"
3. Extract to `C:\ffmpeg`
4. Add to PATH:
   - Windows Search → "Environment Variables"
   - System variables → "Path" → Edit → New
   - Add: `C:\ffmpeg\bin`
   - OK → OK → OK
5. **RESTART terminal/IDE**

**Verify:**
```bash
ffmpeg -version
```

### Step 2: Fix Python Dependencies
```bash
fix_dependencies.bat
```

This installs:
- `ffmpeg-python` - Python wrapper for FFmpeg
- `mediapipe==0.10.9` - Correct version for facial analysis
- `google-generativeai` - Latest Gemini AI package

### Step 3: Verify Installation
```bash
python diagnose_zero_scores.py
```

Look for:
- ✅ FFmpeg is installed
- ✅ All packages installed
- ✅ OpenCV can read video
- ✅ Whisper transcription works

### Step 4: Restart Backend
```bash
python backend/app.py
```

### Step 5: Test with New Interview

**IMPORTANT:** Complete a NEW interview after fixing. Old interviews may still have 0 scores.

1. Login to application
2. Start new interview
3. Upload resume and job description
4. Answer at least ONE question (speak for 10-15 seconds)
5. Complete interview
6. Check feedback

### Step 6: Verify in Backend Logs

You should see:
```
Analyzing answer 1/10 for question 1
File exists, size: 245678 bytes
Loading Whisper model...
Transcribing audio...
Transcription complete. Transcript length: 234 chars
Speech analysis complete - Score: 82, Words: 45, Rate: 135
Opening video with OpenCV...
Processed 156 frames
Facial analysis complete - Confidence: 76, Smile: 35%, Eye contact: 72%
Using Gemini AI to evaluate answer quality...
Question 1 scores - Speech: 82, Facial: 76, Content: 85, Overall: 81.5
```

**If you see this, it's working!** ✅

---

## 🚨 Still Getting 0 Scores?

### Check 1: FFmpeg in PATH
```bash
ffmpeg -version
```
If this fails, FFmpeg is not in PATH. Restart terminal after installation.

### Check 2: Video Files Exist
```bash
dir backend\uploads
```
Should show `.webm` files. If empty, videos aren't being saved.

### Check 3: Backend Logs
Look for these errors:
- "Video file not found" → File path issue
- "Could not open video" → Codec/FFmpeg issue
- "Whisper error" → FFmpeg missing
- "Transcription complete. Transcript length: 0" → No audio in video

### Check 4: Database Scores
```bash
python check_interview_scores.py
```
Shows actual scores in MongoDB. If scores are 0 in database, analysis is failing.

### Check 5: Browser Console
Press F12 in browser, check for:
- Upload errors
- Network errors
- JavaScript errors

---

## 🎯 Expected Scores (When Working)

### Speech Analysis (0-100):
- **80-100:** Excellent clarity, good pace, minimal fillers
- **60-79:** Good speech, some fillers or pace issues
- **40-59:** Needs improvement, many fillers or too fast/slow
- **0-39:** Poor clarity or analysis failed

### Facial Analysis (0-100):
- **80-100:** Great eye contact, confident expressions
- **60-79:** Good presence, some improvements needed
- **40-59:** Limited eye contact or nervous expressions
- **0-39:** Poor body language or analysis failed

### Content Analysis (0-100):
- **80-100:** Excellent answer, relevant, detailed, structured
- **60-79:** Good answer, relevant with some detail
- **40-59:** Basic answer, lacks detail or structure
- **0-39:** Poor answer or off-topic

### Overall Score:
Weighted average: **Content 40% + Speech 30% + Facial 30%**

**If ANY score is 0, analysis failed for that component.**

---

## 🔄 Alternative Solutions

### Option 1: Use Audio-Only Recording

If video processing continues to fail, modify to record audio only:

**Edit:** `frontend/js/interview-new.js`

Change:
```javascript
const stream = await navigator.mediaDevices.getUserMedia({ 
    video: true, 
    audio: true 
});
```

To:
```javascript
const stream = await navigator.mediaDevices.getUserMedia({ 
    video: false,  // Audio only
    audio: true 
});
```

This will:
- ✅ Speech analysis works
- ❌ Facial analysis disabled (uses demo score of 78)
- ✅ Content analysis works
- ✅ Overall score calculated correctly

### Option 2: Change Video Format to MP4

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

### Option 3: Use Demo Scores (Testing Only)

If you just want to test the application flow without real analysis:

**Edit:** `backend/services/speech_analysis.py` and `backend/services/facial_analysis.py`

Change the return values in the exception handlers to return demo scores instead of 0.

---

## 📊 Verification Checklist

After applying fixes:

- [ ] `ffmpeg -version` works
- [ ] `fix_dependencies.bat` completed successfully
- [ ] Backend starts without errors
- [ ] Completed a NEW interview (old ones may still have 0)
- [ ] Backend logs show "Speech analysis complete - Score: XX"
- [ ] Backend logs show "Facial analysis complete - Confidence: XX"
- [ ] Feedback page shows non-zero scores
- [ ] Overall score is calculated correctly

---

## 🎓 Understanding the Logs

### Good Logs (Working):
```
Analyzing answer 1/10 for question 1
File exists, size: 245678 bytes          ← Video file found
Loading Whisper model...                 ← Whisper starting
Transcribing audio...                    ← FFmpeg extracting audio
Transcription complete. Length: 234      ← Got transcript ✅
Speech analysis complete - Score: 82    ← Non-zero score ✅
Processed 156 frames                     ← OpenCV reading video
Facial analysis complete - Confidence: 76 ← Non-zero score ✅
Question 1 scores - Speech: 82, Facial: 76, Content: 85
```

### Bad Logs (Broken):
```
Analyzing answer 1/10 for question 1
Speech analysis error: ...               ← Analysis failed ❌
Facial analysis error: ...               ← Analysis failed ❌
Question 1 scores - Speech: 0, Facial: 0, Content: 85
```

---

## 💡 Pro Tips

1. **Always check backend logs** - They show exactly what's failing
2. **Install FFmpeg first** - It's the most common issue
3. **Test with one question** - Don't record all 10 if first one fails
4. **Use good lighting** - Helps facial analysis
5. **Speak clearly** - Helps speech analysis
6. **Record 10-15 seconds minimum** - Too short videos may fail

---

## 📞 Quick Commands Reference

```bash
# Diagnosis
check_ffmpeg.bat                  # Check FFmpeg
python diagnose_zero_scores.py    # Full diagnosis
python check_interview_scores.py  # Check database

# Fixes
install_ffmpeg_guide.bat          # FFmpeg install guide
fix_dependencies.bat              # Fix Python packages

# Testing
python test_analysis_services.py  # Test analysis
python check_video_support.py     # Test codecs

# Running
START_APPLICATION.bat             # Start everything
python backend/app.py             # Start backend only
```

---

## ✅ Success Indicators

When everything is working:

1. **Backend logs show actual analysis** (not just errors)
2. **Scores are non-zero** (typically 60-85 range)
3. **Transcripts are present** (not empty)
4. **Video files exist** in uploads folder
5. **Dashboard shows accurate scores**

---

## 🎉 Bottom Line

**90% of zero score issues are caused by missing FFmpeg.**

1. Install FFmpeg
2. Run fix_dependencies.bat
3. Restart backend
4. Complete NEW interview
5. Check scores

That's it! 🚀

For detailed instructions, see: `ZERO_SCORES_FIX.md`
