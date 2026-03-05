from flask import Blueprint, request, jsonify, current_app
import jwt
from bson import ObjectId
from services.speech_analysis import analyze_speech
from services.facial_analysis import analyze_facial_expressions
from services.nlp_analysis import analyze_content
from services.gemini_evaluator import evaluate_answer_with_gemini

feedback_bp = Blueprint('feedback', __name__)

def get_db():
    return current_app.db

def verify_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except:
        return None

@feedback_bp.route('/<interview_id>', methods=['GET'])
def get_feedback(interview_id):
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_id = verify_token(token)
        
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        interview = db.interviews.find_one({
            '_id': ObjectId(interview_id),
            'user_id': ObjectId(user_id)
        })
        
        if not interview:
            return jsonify({'error': 'Interview not found'}), 404
        
        # Check if this is a multi-question interview
        answers = interview.get('answers', [])
        questions = interview.get('questions', [])
        
        if answers and len(answers) > 0:
            # Multi-question interview - analyze each answer
            return analyze_multi_question_interview(interview_id, interview, db)
        elif interview.get('video_path'):
            # Legacy single-video interview
            return analyze_single_video_interview(interview_id, interview, db)
        else:
            return jsonify({'error': 'No interview data found'}), 404
        
    except Exception as e:
        print(f"Get feedback error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Failed to get feedback'}), 500

def analyze_multi_question_interview(interview_id, interview, db):
    """Analyze interview with multiple question answers - ALWAYS analyzes ALL answers"""
    
    print(f"Analyzing multi-question interview: {interview_id}")
    
    answers = interview.get('answers', [])
    questions = interview.get('questions', [])
    
    if not answers or len(answers) == 0:
        return jsonify({'error': 'No answers found for this interview'}), 404
    
    print(f"Found {len(answers)} answers to analyze")
    
    # Create question lookup
    question_map = {q['id']: q for q in questions}
    
    # Analyze each answer (FORCE re-analysis for accuracy)
    analyzed_answers = []
    total_speech_score = 0
    total_facial_score = 0
    total_content_score = 0
    analyzed_count = 0
    
    for idx, answer in enumerate(answers):
        video_path = answer.get('video_path')
        question_id = answer.get('question_id')
        
        if not video_path:
            print(f"Skipping answer {idx+1}: No video path")
            analyzed_answers.append(answer)
            continue
        
        print(f"Analyzing answer {idx+1}/{len(answers)} for question {question_id}")
        
        # Get question details
        question_data = question_map.get(question_id, {})
        question_text = question_data.get('question', '')
        question_type = question_data.get('type', 'behavioral')
        
        # Run AI analysis on THIS answer
        speech_results = analyze_speech(video_path)
        facial_results = analyze_facial_expressions(video_path)
        
        # Use Gemini AI for accurate content evaluation
        transcript = speech_results.get('transcript', '')
        if transcript and len(transcript) > 10:
            print(f"Using Gemini AI to evaluate answer quality...")
            gemini_eval = evaluate_answer_with_gemini(question_text, transcript, question_type)
            content_score = gemini_eval.get('overall_score', 70)
            content_results = {
                'relevance_score': content_score,
                'content_score': gemini_eval.get('content_score', 70),
                'communication_score': gemini_eval.get('communication_score', 75),
                'completeness_score': gemini_eval.get('completeness_score', 72),
                'word_count': len(transcript.split()),
                'strengths': gemini_eval.get('strengths', []),
                'improvements': gemini_eval.get('improvements', []),
                'feedback': [gemini_eval.get('feedback_summary', 'Good answer')]
            }
        else:
            # Fallback to basic NLP analysis
            content_results = analyze_content(transcript)
            content_score = content_results.get('relevance_score', 0)
        
        # Calculate question score with proper weighting
        # Speech: 30%, Facial: 30%, Content: 40% (content is most important)
        speech_score = speech_results.get('clarity_score', 0)
        facial_score = facial_results.get('confidence_score', 0)
        question_score = round((speech_score * 0.3) + (facial_score * 0.3) + (content_score * 0.4), 2)
        
        # Store analysis with answer
        answer['analysis'] = {
            'speech_analysis': speech_results,
            'facial_analysis': facial_results,
            'content_analysis': content_results,
            'question_score': question_score,
            'question_text': question_text
        }
        answer['analyzed'] = True
        
        analyzed_answers.append(answer)
        
        # Add to totals
        total_speech_score += speech_score
        total_facial_score += facial_score
        total_content_score += content_score
        analyzed_count += 1
        
        print(f"Question {question_id} scores - Speech: {speech_score}, Facial: {facial_score}, Content: {content_score}, Overall: {question_score}")
    
    print(f"Total analyzed: {analyzed_count} answers")
    
    # Calculate overall scores from ALL answers
    if analyzed_count > 0:
        avg_speech_score = round(total_speech_score / analyzed_count, 2)
        avg_facial_score = round(total_facial_score / analyzed_count, 2)
        avg_content_score = round(total_content_score / analyzed_count, 2)
        overall_score = round((avg_speech_score + avg_facial_score + avg_content_score) / 3, 2)
    else:
        avg_speech_score = 0
        avg_facial_score = 0
        avg_content_score = 0
        overall_score = 0
    
    print(f"Overall scores - Speech: {avg_speech_score}, Facial: {avg_facial_score}, Content: {avg_content_score}, Overall: {overall_score}")
    
    # Find best and worst answers
    scored_answers = [(a, a.get('analysis', {}).get('question_score', 0)) for a in analyzed_answers if a.get('analyzed')]
    scored_answers.sort(key=lambda x: x[1], reverse=True)
    
    best_answer = scored_answers[0] if scored_answers else None
    worst_answer = scored_answers[-1] if scored_answers else None
    
    # Compile feedback
    feedback = {
        'interview_type': 'multi_question',
        'total_questions': len(questions),
        'answered_questions': len(answers),
        'analyzed_questions': analyzed_count,
        'overall_score': overall_score,
        'average_scores': {
            'speech': avg_speech_score,
            'facial': avg_facial_score,
            'content': avg_content_score
        },
        'answers': analyzed_answers,
        'best_answer': {
            'question_id': best_answer[0]['question_id'],
            'score': best_answer[1],
            'question': question_map.get(best_answer[0]['question_id'], {}).get('question', '')
        } if best_answer else None,
        'worst_answer': {
            'question_id': worst_answer[0]['question_id'],
            'score': worst_answer[1],
            'question': question_map.get(worst_answer[0]['question_id'], {}).get('question', '')
        } if worst_answer else None,
        'recommendations': generate_recommendations(avg_speech_score, avg_facial_score, avg_content_score)
    }
    
    # Update database with ALL analyzed answers and overall score
    db.interviews.update_one(
        {'_id': ObjectId(interview_id)},
        {'$set': {
            'feedback': feedback,
            'answers': analyzed_answers,
            'overall_score': overall_score,
            'status': 'completed'
        }}
    )
    
    print(f"Interview {interview_id} analysis complete. Overall score: {overall_score}")
    
    return jsonify(feedback), 200

def analyze_single_video_interview(interview_id, interview, db):
    """Analyze legacy single-video interview"""
    
    if interview.get('feedback'):
        return jsonify(interview['feedback']), 200
    
    video_path = interview['video_path']
    
    print(f"Analyzing single-video interview: {interview_id}")
    speech_results = analyze_speech(video_path)
    facial_results = analyze_facial_expressions(video_path)
    content_results = analyze_content(speech_results.get('transcript', ''))
    
    feedback = {
        'interview_type': 'single_video',
        'speech_analysis': speech_results,
        'facial_analysis': facial_results,
        'content_analysis': content_results,
        'overall_score': calculate_overall_score(speech_results, facial_results, content_results)
    }
    
    db.interviews.update_one(
        {'_id': ObjectId(interview_id)},
        {'$set': {'feedback': feedback, 'status': 'completed', 'overall_score': feedback['overall_score']}}
    )
    
    return jsonify(feedback), 200

def calculate_question_score(speech, facial, content):
    """Calculate score for a single question"""
    speech_score = speech.get('clarity_score', 0)
    confidence_score = facial.get('confidence_score', 0)
    content_score = content.get('relevance_score', 0)
    
    return round((speech_score + confidence_score + content_score) / 3, 2)

def calculate_overall_score(speech, facial, content):
    """Calculate overall score (legacy)"""
    speech_score = speech.get('clarity_score', 0)
    confidence_score = facial.get('confidence_score', 0)
    content_score = content.get('relevance_score', 0)
    
    return round((speech_score + confidence_score + content_score) / 3, 2)

def generate_recommendations(speech_score, facial_score, content_score):
    """Generate personalized recommendations"""
    recommendations = []
    
    if speech_score < 60:
        recommendations.append("Practice speaking more clearly and at a moderate pace. Record yourself and listen back.")
    elif speech_score < 75:
        recommendations.append("Good speech clarity. Work on reducing filler words and pauses.")
    else:
        recommendations.append("Excellent speech delivery! Maintain this level of clarity.")
    
    if facial_score < 60:
        recommendations.append("Improve eye contact and facial expressions. Practice in front of a mirror.")
    elif facial_score < 75:
        recommendations.append("Good body language. Try to appear more relaxed and confident.")
    else:
        recommendations.append("Great confidence and body language!")
    
    if content_score < 60:
        recommendations.append("Structure your answers better. Use the STAR method (Situation, Task, Action, Result).")
    elif content_score < 75:
        recommendations.append("Good content quality. Add more specific examples and details.")
    else:
        recommendations.append("Excellent answer quality with great examples!")
    
    return recommendations
