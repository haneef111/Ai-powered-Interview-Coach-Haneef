# Environment Variables Setup Guide

## 🔐 Secure Credential Management

This project uses environment variables to keep sensitive information (API keys, passwords, database URLs) secure and separate from code.

## 📋 Quick Setup

### Step 1: Copy the Template
```bash
cd backend
copy .env.example .env
```

Or on Mac/Linux:
```bash
cd backend
cp .env.example .env
```

### Step 2: Edit .env File
Open `backend/.env` and fill in your actual values:

```env
SECRET_KEY=your-actual-secret-key
MONGO_URI=your-actual-mongodb-connection-string
GEMINI_API_KEY=your-actual-gemini-api-key
```

### Step 3: Never Commit .env
The `.gitignore` file already excludes `.env` from Git, so your credentials stay safe!

---

## 🔑 Getting Your Credentials

### 1. SECRET_KEY
Generate a secure random key:

**Option A - Python:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Option B - Online:**
Visit: https://randomkeygen.com/

**Example:**
```env
SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
```

### 2. MONGO_URI (MongoDB Atlas)

**Step-by-step:**
1. Go to: https://www.mongodb.com/cloud/atlas
2. Sign up / Login
3. Create a free cluster (M0 Sandbox)
4. Click "Connect" → "Connect your application"
5. Copy the connection string
6. Replace `<password>` with your actual password
7. Add database name at the end

**Example:**
```env
MONGO_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/interview_coach?retryWrites=true&w=majority
```

**Important:** 
- Replace `username` with your MongoDB username
- Replace `password` with your MongoDB password
- URL-encode special characters in password:
  - `@` becomes `%40`
  - `#` becomes `%23`
  - `$` becomes `%24`

### 3. GEMINI_API_KEY (Google AI)

**Step-by-step:**
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key

**Example:**
```env
GEMINI_API_KEY=AIzaSyAaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQq
```

---

## 📁 File Structure

```
project/
├── .gitignore              ← Excludes .env from Git
├── backend/
│   ├── .env               ← YOUR CREDENTIALS (never commit!)
│   ├── .env.example       ← Template (safe to commit)
│   └── config.py          ← Reads from .env
```

---

## ✅ Verification

### Check if .env is loaded:
```bash
cd backend
python -c "from config import Config; print('MongoDB:', Config.MONGO_URI[:20]); print('Gemini:', Config.GEMINI_API_KEY[:20])"
```

Should show:
```
MongoDB: mongodb+srv://usern
Gemini: AIzaSyAaBbCcDdEeFf
```

### Check if .env is ignored by Git:
```bash
git status
```

Should NOT show `.env` in the list!

---

## 🚨 Security Best Practices

### ✅ DO:
- ✅ Keep `.env` file local only
- ✅ Use `.env.example` as template
- ✅ Add `.env` to `.gitignore`
- ✅ Use different credentials for dev/prod
- ✅ Rotate API keys regularly
- ✅ Use strong, random SECRET_KEY

### ❌ DON'T:
- ❌ Commit `.env` to Git
- ❌ Share `.env` file publicly
- ❌ Hardcode credentials in code
- ❌ Use same credentials everywhere
- ❌ Share API keys in screenshots
- ❌ Post credentials in issues/forums

---

## 🔄 For Team Members

When someone clones your repository:

1. They get `.env.example` (template)
2. They copy it to `.env`
3. They fill in their own credentials
4. Their `.env` stays local (not committed)

**Share this guide with them!**

---

## 🌐 Deployment (Production)

### For Heroku:
```bash
heroku config:set SECRET_KEY=your-key
heroku config:set MONGO_URI=your-uri
heroku config:set GEMINI_API_KEY=your-key
```

### For AWS/Azure/GCP:
Use their environment variable management:
- AWS: Systems Manager Parameter Store
- Azure: App Configuration
- GCP: Secret Manager

### For Docker:
```bash
docker run -e SECRET_KEY=your-key -e MONGO_URI=your-uri ...
```

Or use docker-compose.yml with env_file:
```yaml
services:
  backend:
    env_file:
      - .env
```

---

## 🔍 Troubleshooting

### "Config not loading .env"
- Check `.env` is in `backend/` folder
- Check file is named exactly `.env` (not `.env.txt`)
- Restart your backend server

### "MongoDB connection failed"
- Check MONGO_URI is correct
- Check password is URL-encoded
- Check IP whitelist in MongoDB Atlas
- Test connection string in MongoDB Compass

### "Gemini API error"
- Check GEMINI_API_KEY is correct
- Check API key is enabled
- Check you have API quota remaining
- Try regenerating the key

### ".env file showing in Git"
- Check `.gitignore` exists in root folder
- Check `.env` is listed in `.gitignore`
- Run: `git rm --cached backend/.env`
- Commit the removal

---

## 📝 Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes | - | Flask secret key for sessions |
| `MONGO_URI` | Yes | - | MongoDB connection string |
| `GEMINI_API_KEY` | Yes | - | Google Gemini AI API key |
| `JWT_EXPIRATION_HOURS` | No | 24 | JWT token expiration time |
| `UPLOAD_FOLDER` | No | uploads | Folder for uploaded files |
| `MAX_VIDEO_SIZE` | No | 104857600 | Max upload size (100MB) |
| `FLASK_ENV` | No | development | Flask environment |
| `FLASK_DEBUG` | No | True | Enable debug mode |

---

## 🎯 Quick Commands

### Create .env from template:
```bash
cd backend
copy .env.example .env
```

### Generate SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Test configuration:
```bash
cd backend
python -c "from config import Config; print('Config loaded successfully!')"
```

### Check Git status:
```bash
git status
# .env should NOT appear here
```

---

## ✅ Checklist

Before committing to GitHub:

- [ ] `.env` file exists in `backend/`
- [ ] `.env` contains your actual credentials
- [ ] `.env.example` exists (template only)
- [ ] `.gitignore` includes `.env`
- [ ] `git status` does NOT show `.env`
- [ ] `config.py` uses `os.getenv()`
- [ ] Application runs with credentials from `.env`

---

## 🎉 You're Secure!

Your credentials are now:
- ✅ Stored locally in `.env`
- ✅ Excluded from Git
- ✅ Safe to push to GitHub
- ✅ Easy to manage

**Remember:** Never commit `.env` to GitHub!
