# AI-Powered Interview Coach

An intelligent platform for mock interview practice with AI-driven feedback on voice, expressions, and content quality.

## 🚀 Quick Start

### Fastest Way to Run:
1. **Install FFmpeg** (REQUIRED): `check_ffmpeg.bat`
2. **Fix dependencies**: `fix_dependencies.bat`
3. **Start app**: `START_APPLICATION.bat`
4. **Open browser**: http://localhost:8000

---
- 🎤 Voice & tone analysis (speech rate, clarity, filler words)
- 😊 Facial expression & body language tracking (eye contact, confidence)
- 🤖 AI-powered answer evaluation using Google Gemini
- 📄 Resume and job description analysis
- 🎯 Personalized question generation (10 questions per interview)
- 📊 Comprehensive feedback dashboard with history
- 🔐 Secure authentication with JWT
- 📈 Progress tracking across multiple interviews

## Tech Stack
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python 3.13.2, Flask
- **Database:** MongoDB Atlas
- **AI/ML:** 
  - Google Gemini AI (question generation & answer evaluation)
  - OpenAI Whisper (speech-to-text)
  - OpenCV + MediaPipe (facial analysis)
  - NLP models (content analysis)

## Prerequisites

### Required:
- Python 3.8+ (tested with 3.13.2)
- **FFmpeg** (CRITICAL for speech analysis)
- MongoDB Atlas account (or local MongoDB)
- Modern web browser with camera/microphone
- Internet connection

### Manual Setup:

### Manual Setup:

1. **Install FFmpeg** (if not already installed)
   ```bash
   choco install ffmpeg
   # OR see install_ffmpeg_guide.bat
   ```

2. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   - Copy `backend/.env.example` to `backend/.env`
   - Add your credentials:
     - MongoDB URI
     - Gemini API key
     - Secret key

4. **Start backend:**
   ```bash
   python backend/app.py
   ```

5. **Start frontend** (new terminal):
   ```bash
   cd frontend
   python -m http.server 8000
   ```

6. **Open browser:**
   http://localhost:8000

## Usage

1. **Sign Up / Login**
2. **Start New Interview**
   - Upload your resume (PDF/DOCX/TXT)
   - Paste job description
   - Click "Generate Questions"
3. **Answer Questions**
   - 10 AI-generated questions based on your resume
   - Record video answer for each question
   - Look at camera for best results
4. **Get Feedback**
   - Overall score (0-100)
   - Speech, facial, and content breakdown
   - Question-by-question analysis
   - AI-powered recommendations
5. **Track Progress**
   - View interview history
   - Compare scores over time
   - Identify improvement areas

### Other Issues:
- **MongoDB connection failed:** Check internet and credentials in `.env`
- **Port already in use:** Close other apps or change port
- **Camera not working:** Allow browser permissions
- **Questions not generating:** Check Gemini API key in `.env`

## Documentation

- `README_START_HERE.md` - Quickest way to get started
- `QUICK_START_GUIDE.md` - Detailed usage guide
- `COMPLETE_SETUP_GUIDE.md` - Full setup instructions
- `ENVIRONMENT_SETUP.md` - Environment configuration
- `GEMINI_AI_INTEGRATION.md` - Gemini AI details
- `ZERO_SCORES_FIX.md` - Fix zero scores issue
- `TROUBLESHOOTING_ZERO_SCORES.md` - Comprehensive troubleshooting

## Project Structure

```
├── backend/
│   ├── app.py                    # Main Flask application
│   ├── config.py                 # Configuration
│   ├── .env                      # Environment variables (not in Git)
│   ├── routes/                   # API endpoints
│   ├── services/                 # AI analysis services
│   └── uploads/                  # User uploads
├── frontend/
│   ├── *.html                    # Web pages
│   ├── js/                       # JavaScript files
│   └── css/                      # Stylesheets
├── START_APPLICATION.bat         # One-click start
├── fix_dependencies.bat          # Fix Python packages
├── check_ffmpeg.bat              # Check FFmpeg
└── run_all_diagnostics.bat       # Run all checks
```

## Contributing

This is a project for interview preparation. Feel free to extend and customize for your needs.

## License

MIT License - Feel free to use and modify.

---

**Need help?** Start with `README_START_HERE.md` or run `run_all_diagnostics.bat` to check your setup.

