# Quick Start Guide - AI Interview Coach

## 🚀 Easiest Way to Run

### Option 1: One-Click Start (Recommended)
**Double-click:** `START_APPLICATION.bat`

This will:
1. Start the backend server (port 5000)
2. Start the frontend server (port 8000)
3. Open your browser automatically
4. You're ready to go!

---

## 📋 Manual Start (Alternative)

### Step 1: Start Backend
Open Command Prompt #1:
```bash
cd backend
python app.py
```

You should see:
```
✓ Connected to MongoDB successfully!
🚀 AI Interview Coach Backend Starting...
🌐 Server: http://localhost:5000
```

**Keep this window open!**

### Step 2: Start Frontend
Open Command Prompt #2:
```bash
cd frontend
python -m http.server 8000
```

You should see:
```
Serving HTTP on :: port 8000 (http://[::]:8000/) ...
```

**Keep this window open!**

### Step 3: Open Browser
Go to: **http://localhost:8000**

---

## 🎯 Using the Application

### First Time Setup:
1. Click **"Sign Up"**
2. Enter your details:
   - Name
   - Email
   - Password
   - Job Role (optional)
   - Industry (optional)
3. Click **"Sign Up"**
4. You'll be logged in automatically

### Start an Interview:
1. Click **"Start New Interview"** on dashboard
2. **Upload your resume** (PDF, DOCX, or TXT)
3. **Paste job description** from the job posting
4. Click **"Generate Questions"**
5. Review the 10 AI-generated questions
6. Click **"Start Interview"**

### During Interview:
1. Allow camera and microphone access
2. Read the question
3. Click **"Start Recording"**
4. Answer the question (look at camera!)
5. Click **"Stop Recording"**
6. Click **"Next Question"**
7. Repeat for all 10 questions
8. Click **"Finish Interview"**

### View Feedback:
1. Wait for analysis (takes 1-2 minutes)
2. See your overall score
3. Review question-by-question breakdown
4. Read AI-powered recommendations
5. Check best and worst answers

### View History:
1. Go to **Dashboard**
2. See all your past interviews
3. Click **"View Feedback"** on any interview
4. Track your progress over time

---

## 🔧 Troubleshooting

### Backend won't start:
**Error:** `Port 5000 already in use`
- Close any other programs using port 5000
- Or change port in `backend/app.py` (last line)

**Error:** `MongoDB connection failed`
- Check your internet connection
- Verify MongoDB Atlas credentials in `backend/config.py`
- Or use SQLite version: `python app_sqlite.py`

**Error:** `Module not found`
- Install dependencies: `pip install -r requirements.txt`
- Or run: `fix_dependencies.bat`

### Frontend won't start:
**Error:** `Port 8000 already in use`
- Use different port: `python -m http.server 8001`
- Then open: `http://localhost:8001`

### Browser shows blank page:
- Make sure both backend AND frontend are running
- Check browser console (F12) for errors
- Try: `http://127.0.0.1:8000` instead

### Camera/Microphone not working:
- Allow permissions when browser asks
- Use Chrome or Edge (best compatibility)
- Check if camera is used by another app
- Try refreshing the page

### Questions not generating:
- Check backend terminal for errors
- Verify Gemini API key in `backend/config.py`
- Check internet connection
- System will use default questions if AI fails

### Upload fails:
- Check file size (max 5MB)
- Use supported formats: PDF, DOCX, TXT
- Check backend terminal for error messages

---

## 📊 System Requirements

### Required:
- Python 3.8 or higher
- Modern web browser (Chrome, Edge, Firefox)
- Internet connection (for MongoDB Atlas and Gemini AI)
- Webcam and microphone

### Recommended:
- Python 3.10 or 3.11
- Chrome browser (best compatibility)
- Stable internet connection
- Good lighting for camera

---

## 🛑 Stopping the Application

### If using START_APPLICATION.bat:
- Close the two Command Prompt windows that opened
- Or press Ctrl+C in each window

### If started manually:
- Press Ctrl+C in the backend window
- Press Ctrl+C in the frontend window

---

## 📁 Important Files

### Configuration:
- `backend/config.py` - API keys and settings
- `backend/.env` - Environment variables

### Data:
- `backend/uploads/` - Uploaded resumes and videos
- MongoDB Atlas - User data and interviews

### Logs:
- Backend terminal - Server logs and errors
- Browser console (F12) - Frontend errors

---

## 🎓 Tips for Best Results

### Resume Upload:
- Use clear, well-formatted resume
- Include skills section
- Mention years of experience
- List education and certifications

### Job Description:
- Paste complete job posting
- Include required skills
- Include responsibilities
- Include qualifications

### During Interview:
- **Look at the camera** (eye contact)
- **Speak clearly** at moderate pace
- **Avoid filler words** (um, uh, like)
- **Use STAR method** (Situation, Task, Action, Result)
- **Give specific examples** from your experience
- **Keep answers 1-2 minutes** long

### After Interview:
- Review feedback carefully
- Focus on lowest-scoring areas
- Practice weak questions again
- Track improvement over time
- Try different job descriptions

---

## 🆘 Need Help?

### Check These First:
1. Both backend and frontend are running
2. No error messages in terminals
3. Browser console (F12) shows no errors
4. Internet connection is stable
5. Camera/microphone permissions granted

### Common Issues:
- **"Server error"** → Backend not running or crashed
- **"Unauthorized"** → Login again
- **"Upload failed"** → Check file size and format
- **"Analysis failed"** → Check backend logs
- **Blank page** → Frontend not running

### Still Having Issues?
1. Check `FIX_ERRORS_GUIDE.md`
2. Check `COMPLETE_SETUP_GUIDE.md`
3. Check `GEMINI_AI_INTEGRATION.md`
4. Look at backend terminal for error messages
5. Look at browser console (F12) for errors

---

## ✅ Quick Checklist

Before starting interview:
- [ ] Backend running (port 5000)
- [ ] Frontend running (port 8000)
- [ ] Logged in to account
- [ ] Resume ready (PDF/DOCX/TXT)
- [ ] Job description copied
- [ ] Camera working
- [ ] Microphone working
- [ ] Good lighting
- [ ] Quiet environment

---

## 🎉 You're Ready!

1. **Double-click** `START_APPLICATION.bat`
2. **Sign up** or **Login**
3. **Start interview** with resume and job description
4. **Answer questions** with confidence
5. **Get AI-powered feedback**
6. **Improve and practice**

Good luck with your interview preparation! 🚀
