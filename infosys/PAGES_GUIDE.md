# Pages Guide - AI Interview Coach

## Frontend Pages

### 1. index.html (Homepage)
- Landing page with features
- Links to Login and Sign Up
- URL: http://localhost:8000/

### 2. login.html (Login Page)
- Simple login form (email + password only)
- Link to signup page
- URL: http://localhost:8000/login.html
- Script: js/login.js

### 3. signup.html (Sign Up Page)
- Registration form with all fields
- Name, Email, Password, Job Role, Industry
- Link to login page
- URL: http://localhost:8000/signup.html
- Script: js/signup.js

### 4. dashboard.html (User Dashboard)
- Shows after successful login
- Start new interview button
- Interview history
- URL: http://localhost:8000/dashboard.html
- Script: js/dashboard.js

### 5. interview.html (Mock Interview)
- Video recording interface
- Interview questions
- Submit interview
- URL: http://localhost:8000/interview.html
- Script: js/interview.js

### 6. feedback.html (AI Feedback)
- Shows after interview submission
- Speech, facial, and content analysis
- Overall score
- URL: http://localhost:8000/feedback.html
- Script: js/feedback.js

## Navigation Flow

```
index.html
    ↓
    ├─→ login.html → dashboard.html → interview.html → feedback.html
    └─→ signup.html → dashboard.html → interview.html → feedback.html
```

## Backend Routes

### Authentication
- POST /api/auth/register - Create new account
- POST /api/auth/login - Login to existing account

### Interview
- GET /api/interview/questions - Get interview questions
- POST /api/interview/submit - Submit recorded interview

### Feedback
- GET /api/feedback/<interview_id> - Get AI analysis results

## Testing the Pages

1. Start backend: `cd backend && python app.py`
2. Start frontend: `cd frontend && python -m http.server 8000`
3. Open: http://localhost:8000
4. Click "Sign Up" to create account
5. Or click "Login" if you already have an account
