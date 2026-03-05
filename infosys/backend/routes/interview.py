from flask import Blueprint, request, jsonify, current_app
import jwt
import os
from datetime import datetime
from bson import ObjectId
from werkzeug.utils import secure_filename
from services.document_processor import extract_text, analyze_document
from services.question_generator import generate_questions_from_analysis, generate_default_questions

interview_bp = Blueprint('interview', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def get_db():
    return current_app.db

def verify_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except:
        return None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@interview_bp.route('/upload-documents', methods=['POST'])
def upload_documents():
    """Upload resume and job description, generate personalized questions"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_id = verify_token(token)
        
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        # Get job description text
        job_description = request.form.get('job_description', '')
        
        # Handle resume file upload
        resume_text = ""
        resume_path = None
        
        if 'resume' in request.files:
            resume_file = request.files['resume']
            if resume_file and allowed_file(resume_file.filename):
                filename = secure_filename(f"{user_id}_resume_{datetime.utcnow().timestamp()}.{resume_file.filename.rsplit('.', 1)[1]}")
                resume_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                resume_file.save(resume_path)
                resume_text = extract_text(resume_path)
        
        # Analyze documents
        resume_analysis = analyze_document(resume_text, 'resume') if resume_text else {}
        job_analysis = analyze_document(job_description, 'job_description') if job_description else {}
        
        # Generate questions
        if resume_analysis and job_analysis:
            questions = generate_questions_from_analysis(resume_analysis, job_analysis)
        else:
            questions = generate_default_questions()
        
        # Create interview session
        interview_session = {
            'user_id': ObjectId(user_id),
            'resume_path': resume_path,
            'resume_analysis': resume_analysis,
            'job_description': job_description,
            'job_analysis': job_analysis,
            'questions': questions,
            'answers': [],
            'created_at': datetime.utcnow(),
            'status': 'pending',
            'overall_score': None
        }
        
        result = db.interviews.insert_one(interview_session)
        
        return jsonify({
            'interview_id': str(result.inserted_id),
            'questions': questions,
            'resume_skills': resume_analysis.get('skills', []),
            'job_skills': job_analysis.get('skills', [])
        }), 201
        
    except Exception as e:
        print(f"Upload documents error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Failed to process documents'}), 500

@interview_bp.route('/questions', methods=['GET'])
def get_questions():
    """Get default interview questions (legacy endpoint)"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_id = verify_token(token)
        
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        questions = generate_default_questions()
        return jsonify({'questions': [q['question'] for q in questions]}), 200
        
    except Exception as e:
        print(f"Get questions error: {e}")
        return jsonify({'error': 'Failed to load questions'}), 500

@interview_bp.route('/<interview_id>/submit-answer', methods=['POST'])
def submit_answer(interview_id):
    """Submit answer for a specific question"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_id = verify_token(token)
        
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        print(f"Submit answer - Interview ID: {interview_id}, User ID: {user_id}")
        
        # Get question_id from form data
        question_id_str = request.form.get('question_id')
        if not question_id_str:
            return jsonify({'error': 'Missing question_id'}), 400
        
        try:
            question_id = int(question_id_str)
        except ValueError:
            return jsonify({'error': 'Invalid question_id'}), 400
        
        # Handle video upload
        if 'video' not in request.files:
            return jsonify({'error': 'No video file'}), 400
        
        file = request.files['video']
        if file.filename == '':
            return jsonify({'error': 'Empty file'}), 400
        
        filename = secure_filename(f"{user_id}_{interview_id}_q{question_id}_{datetime.utcnow().timestamp()}.webm")
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        print(f"Saving video to: {filepath}")
        file.save(filepath)
        
        # Store answer
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        answer_data = {
            'question_id': question_id,
            'video_path': filepath,
            'submitted_at': datetime.utcnow(),
            'analyzed': False
        }
        
        result = db.interviews.update_one(
            {'_id': ObjectId(interview_id), 'user_id': ObjectId(user_id)},
            {'$push': {'answers': answer_data}}
        )
        
        if result.modified_count == 0:
            print(f"Warning: No interview updated for ID {interview_id}")
            return jsonify({'error': 'Interview not found or not updated'}), 404
        
        print(f"Answer submitted successfully for question {question_id}")
        return jsonify({'success': True, 'message': 'Answer submitted'}), 200
        
    except Exception as e:
        print(f"Submit answer error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to submit answer: {str(e)}'}), 500

@interview_bp.route('/submit', methods=['POST'])
def submit_interview():
    """Submit complete interview (legacy endpoint for single video)"""
    try:
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
        
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        interview = {
            'user_id': ObjectId(user_id),
            'video_path': filepath,
            'created_at': datetime.utcnow(),
            'status': 'processing',
            'questions': generate_default_questions(),
            'answers': []
        }
        
        result = db.interviews.insert_one(interview)
        
        return jsonify({'interview_id': str(result.inserted_id), 'status': 'processing'}), 201
        
    except Exception as e:
        print(f"Submit interview error: {e}")
        return jsonify({'error': 'Failed to submit interview'}), 500

@interview_bp.route('/<interview_id>/complete', methods=['POST'])
def complete_interview():
    """Mark interview as complete and trigger analysis"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_id = verify_token(token)
        
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        # Update interview status
        db.interviews.update_one(
            {'_id': ObjectId(interview_id), 'user_id': ObjectId(user_id)},
            {'$set': {'status': 'completed', 'completed_at': datetime.utcnow()}}
        )
        
        return jsonify({'success': True, 'message': 'Interview completed'}), 200
        
    except Exception as e:
        print(f"Complete interview error: {e}")
        return jsonify({'error': 'Failed to complete interview'}), 500

@interview_bp.route('/history', methods=['GET'])
def get_interview_history():
    """Get all interviews for the logged-in user"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_id = verify_token(token)
        
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        interviews = list(db.interviews.find(
            {'user_id': ObjectId(user_id)},
            {'video_path': 0, 'answers.video_path': 0}  # Exclude video paths
        ).sort('created_at', -1))
        
        # Convert ObjectId to string
        for interview in interviews:
            interview['_id'] = str(interview['_id'])
            interview['user_id'] = str(interview['user_id'])
        
        return jsonify({'interviews': interviews}), 200
        
    except Exception as e:
        print(f"Get history error: {e}")
        return jsonify({'error': 'Failed to load interview history'}), 500
