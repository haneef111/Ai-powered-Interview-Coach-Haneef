# Setup Guide - AI Interview Coach

## Step 1: Install MongoDB

### Option A: MongoDB Community Edition (Recommended)
1. Download MongoDB from: https://www.mongodb.com/try/download/community
2. Install with default settings
3. MongoDB will run automatically on `mongodb://localhost:27017`

### Option B: MongoDB Atlas (Cloud - Free)
1. Go to https://www.mongodb.com/cloud/atlas/register
2. Create a free cluster
3. Get your connection string and update it in `.env` file

## Step 2: Install Python Dependencies

Open Command Prompt in the `backend` folder and run:

```bash
cd backend
pip install -r requirements.txt
```

If you get errors, try:
```bash
pip install numpy scipy
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

## Step 3: Configure Environment Variables

1. Copy `.env.example` to `.env`:
```bash
copy .env.example .env
```

2. Open `.env` and update:
```
SECRET_KEY=your-generated-secret-key-here
MONGO_URI=mongodb://localhost:27017/interview_coach
```

The SECRET_KEY is already set to a secure random value - you can keep it or generate a new one.

## Step 4: Run the Backend Server

In the `backend` folder:
```bash
python app.py
```

You should see:
```
* Running on http://0.0.0.0:5000
```

## Step 5: Open the Frontend

1. Open `frontend/index.html` in your web browser
2. Or use a local server (recommended):
```bash
cd frontend
python -m http.server 8000
```
Then open: http://localhost:8000

## Step 6: Test the Application

1. Click "Get Started" or "Login"
2. Register a new account
3. Start a mock interview
4. Allow camera/microphone access when prompted
5. Answer questions and get AI feedback!

## Troubleshooting

### MongoDB not running?
- Windows: Open Services and start "MongoDB Server"
- Or run: `mongod` in Command Prompt

### Port 5000 already in use?
Change the port in `backend/app.py` (last line):
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Camera/Microphone not working?
- Check browser permissions
- Use HTTPS or localhost (required for media access)
- Try Chrome or Edge browser

### CORS errors?
Make sure the backend is running on port 5000, or update the API_URL in frontend JS files.
