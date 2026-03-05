from flask import Blueprint, request, jsonify, current_app
import jwt
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import sqlite3

interview_bp = Blueprint('interview', __name__)

def get_db():
    conn = sqlite3.connect('interview_coach.db')
    conn.row_factory = sqlite3.Row
    return conn

def verify_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except:
        return None

@interview_bp.route('/questions', methods=['GET'])
def get_questions():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    user_id = verify_token(token)
    
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Sample questions
    questions = [
        "Tell me about yourself and your background.",
        "What are your greatest strengths?",
        "Describe a challenging situation you faced and how you handled it.",
        "Why do you want to work in this role?",
        "Where do you see yourself in 5 years?"
    ]
    
    return jsonify({'questions': questions}), 200

@interview_bp.route('/submit', methods=['POST'])
def submit_interview():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    user_id = verify_token(token)
    
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if 'video' not in request.files:
        return jsonify({'error': 'No video file'}), 400
    
    file = request.files['video']
    filename = secure_filename(f"{user_id}_{datetime.utcnow().timestamp()}.webm")
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Store interview in database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO interviews (user_id, video_path, status)
        VALUES (?, ?, 'processing')
    ''', (user_id, filepath))
    
    interview_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'interview_id': interview_id, 'status': 'processing'}), 201
