from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
import os
import sqlite3

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# SQLite database setup
DATABASE = 'interview_coach.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize SQLite database with required tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL,
            name TEXT NOT NULL,
            job_role TEXT,
            industry TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Interviews table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            video_path TEXT NOT NULL,
            status TEXT DEFAULT 'processing',
            feedback TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✓ Database initialized successfully!")

# Initialize database on startup
init_db()

# Create uploads directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Import routes
from routes.auth_sqlite import auth_bp
from routes.interview_sqlite import interview_bp
from routes.feedback_sqlite import feedback_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(interview_bp, url_prefix='/api/interview')
app.register_blueprint(feedback_bp, url_prefix='/api/feedback')

@app.route('/')
def index():
    return jsonify({'message': 'AI Interview Coach API', 'status': 'running', 'database': 'SQLite'})

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'database': 'SQLite'})

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 AI Interview Coach Backend Starting...")
    print("="*50)
    print(f"📊 Database: SQLite ({DATABASE})")
    print(f"🌐 Server: http://localhost:5000")
    print(f"📁 Uploads: {app.config['UPLOAD_FOLDER']}")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
