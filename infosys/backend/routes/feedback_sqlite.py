from flask import Blueprint, request, jsonify, current_app
import jwt
import sqlite3
import json
from services.speech_analysis import analyze_speech
from services.facial_analysis import analyze_facial_expressions
from services.nlp_analysis import analyze_content

feedback_bp = Blueprint('feedback', __name__)

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

@feedback_bp.route('/<int:interview_id>', methods=['GET'])
def get_feedback(interview_id):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    user_id = verify_token(token)
    
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM interviews WHERE id = ? AND user_id = ?', 
                   (interview_id, user_id))
    interview = cursor.fetchone()
    
    if not interview:
        conn.close()
        return jsonify({'error': 'Interview not found'}), 404
    
    # Check if analysis is complete
    if interview['status'] == 'processing':
        video_path = interview['video_path']
        
        # Run AI analysis
        speech_results = analyze_speech(video_path)
        facial_results = analyze_facial_expressions(video_path)
        content_results = analyze_content(speech_results.get('transcript', ''))
        
        feedback = {
            'speech_analysis': speech_results,
            'facial_analysis': facial_results,
            'content_analysis': content_results,
            'overall_score': calculate_overall_score(speech_results, facial_results, content_results)
        }
        
        # Update database
        cursor.execute('''
            UPDATE interviews 
            SET feedback = ?, status = 'completed'
            WHERE id = ?
        ''', (json.dumps(feedback), interview_id))
        conn.commit()
        conn.close()
        
        return jsonify(feedback), 200
    
    # Return existing feedback
    feedback = json.loads(interview['feedback']) if interview['feedback'] else {}
    conn.close()
    return jsonify(feedback), 200

def calculate_overall_score(speech, facial, content):
    speech_score = speech.get('clarity_score', 0)
    confidence_score = facial.get('confidence_score', 0)
    content_score = content.get('relevance_score', 0)
    
    return round((speech_score + confidence_score + content_score) / 3, 2)
