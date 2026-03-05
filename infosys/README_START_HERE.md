# 🚀 START HERE - AI Interview Coach

## ⚠️ IMPORTANT: Install FFmpeg First!

**Speech and facial analysis REQUIRE FFmpeg to work.**

### Quick FFmpeg Check:
```bash
check_ffmpeg.bat
```

### Install FFmpeg:
**Option 1 (Easiest):**
```bash
choco install ffmpeg
```

**Option 2 (Manual):**
1. Download: https://www.gyan.dev/ffmpeg/builds/
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to PATH
4. Restart terminal

**Without FFmpeg, you'll get 0 scores for speech and facial analysis!**

---

## ⚡ Quick Start (3 Easy Steps)

### Step 1: Fix Dependencies (First Time Only)
**Double-click:** `fix_dependencies.bat`

This installs all required packages and checks FFmpeg.

### Step 2: Start Application
**Double-click:** `START_APPLICATION.bat`

This starts both backend and frontend automatically!

### Step 3: Use the App
Browser opens automatically at: **http://localhost:8000**

---

## 📖 What You'll See

### Two Command Windows Will Open:

**Window 1 - Backend Server:**
```
✓ Connected to MongoDB successfully!
🚀 AI Interview Coach Backend Starting...
🌐 Server: http://localhost:5000
📁 Uploads: uploads
```
✅ **Keep this window open!**

**Window 2 - Frontend Server:**
```
Serving HTTP on :: port 8000 (http://[::]:8000/) ...
```
✅ **Keep this window open!**

### Browser Opens Automatically:
You'll see the AI Interview Coach homepage!

---

## 🎯 Your First Interview

1. **Sign Up** (top right)
   - Enter name, email, password
   - Click "Sign Up"

2. **Start New Interview** (dashboard)
   - Upload your resume (PDF/DOCX/TXT)
   - Paste job description
   - Click "Generate Questions"

3. **Answer Questions**
   - Allow camera/microphone
   - Click "Start Recording"
   - Answer the question
   - Click "Stop Recording"
   - Click "Next Question"
   - Repeat for all 10 questions

4. **Get Feedback**
   - Click "Finish Interview"
   - Wait for AI analysis
   - See your scores and feedback!

---

## 🛑 To Stop

Close the two Command Prompt windows, or press Ctrl+C in each.

---

## 📚 More Help

- **Zero Scores Issue:** `ZERO_SCORES_FIX.md` ⭐ **START HERE if scores are 0**
- **Quick Start Guide:** `QUICK_START_GUIDE.md`
- **Fix Errors:** `FIX_ERRORS_GUIDE.md`
- **Gemini AI Info:** `GEMINI_AI_INTEGRATION.md`
- **Complete Setup:** `COMPLETE_SETUP_GUIDE.md`

---

## 🔧 Troubleshooting Zero Scores

If speech and facial scores show 0:

```bash
# Step 1: Diagnose the issue
python diagnose_zero_scores.py

# Step 2: Check FFmpeg
check_ffmpeg.bat

# Step 3: Fix dependencies
fix_dependencies.bat

# Step 4: Restart backend
python backend/app.py
```

**See `ZERO_SCORES_FIX.md` for detailed fix instructions.**

---

## 🎉 That's It!

You're ready to practice interviews with AI-powered feedback!

**Need help?** Check `QUICK_START_GUIDE.md` for detailed instructions.
