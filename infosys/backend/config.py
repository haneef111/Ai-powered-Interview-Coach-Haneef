import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key-change-in-production')
    
    # MongoDB
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/interview_coach')
    
    # Google Gemini AI
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    
    # JWT
    JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', 24))
    
    # File Upload
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_VIDEO_SIZE = int(os.getenv('MAX_VIDEO_SIZE', 100 * 1024 * 1024))  # 100MB default
    ALLOWED_EXTENSIONS = {'mp4', 'webm', 'wav', 'mp3', 'pdf', 'docx', 'txt'}
    
    # Flask
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
