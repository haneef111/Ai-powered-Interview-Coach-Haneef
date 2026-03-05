from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# MongoDB connection
try:
    client = MongoClient(app.config['MONGO_URI'], serverSelectionTimeoutMS=5000)
    db = client['interview_coach']
    # Test connection
    client.server_info()
    print("✓ Connected to MongoDB successfully!")
except Exception as e:
    print(f"✗ MongoDB connection failed: {e}")
    db = None

# Store db in app context
app.db = db

# Create uploads directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Import routes
from routes.auth import auth_bp
from routes.interview import interview_bp
from routes.feedback import feedback_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(interview_bp, url_prefix='/api/interview')
app.register_blueprint(feedback_bp, url_prefix='/api/feedback')

@app.route('/')
def index():
    return jsonify({'message': 'AI Interview Coach API', 'status': 'running'})

@app.route('/api/health')
def health():
    db_status = 'connected' if app.db is not None else 'disconnected'
    return jsonify({'status': 'healthy', 'database': db_status})

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 AI Interview Coach Backend Starting...")
    print("="*50)
    print(f"🌐 Server: http://localhost:5000")
    print(f"📁 Uploads: {app.config['UPLOAD_FOLDER']}")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
