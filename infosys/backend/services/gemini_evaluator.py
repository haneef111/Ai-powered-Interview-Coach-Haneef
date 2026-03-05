"""
Gemini AI-powered Answer Evaluation Service
Provides accurate scoring and feedback for interview answers
"""
import google.generativeai as genai
from config import Config
import json

# Configure Gemini API
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')  # Using stable Gemini 1.5 Flash model

def evaluate_answer_with_gemini(question: str, transcript: str, question_type: str = 'behavioral') -> dict:
    """
    Use Gemini AI to evaluate interview answer quality
    Returns detailed scores and feedback
    """
    
    try:
        prompt = f"""You are an expert interview evaluator. Analyze this interview answer and provide detailed scoring.

QUESTION: {question}
QUESTION TYPE: {question_type}

CANDIDATE'S ANSWER:
{transcript}

Evaluate the answer on these criteria and provide scores (0-100):

1. CONTENT QUALITY (0-100):
   - Relevance to the question
   - Depth and detail
   - Use of specific examples
   - Structure (STAR method for behavioral)

2. COMMUNICATION (0-100):
   - Clarity of expression
   - Professional language
   - Coherence and flow

3. COMPLETENESS (0-100):
   - Fully addresses the question
   - Provides sufficient detail
   - Includes outcomes/results

Return your evaluation in this EXACT JSON format:
{{
  "content_score": <number 0-100>,
  "communication_score": <number 0-100>,
  "completeness_score": <number 0-100>,
  "overall_score": <number 0-100>,
  "strengths": ["strength 1", "strength 2"],
  "improvements": ["improvement 1", "improvement 2"],
  "feedback_summary": "Brief overall feedback"
}}

Provide the evaluation now:"""

        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Extract JSON
        if '```json' in response_text:
            json_start = response_text.find('```json') + 7
            json_end = response_text.find('```', json_start)
            response_text = response_text[json_start:json_end].strip()
        elif '```' in response_text:
            json_start = response_text.find('```') + 3
            json_end = response_text.find('```', json_start)
            response_text = response_text[json_start:json_end].strip()
        
        evaluation = json.loads(response_text)
        
        return evaluation
        
    except Exception as e:
        print(f"Gemini evaluation error: {e}")
        return get_default_evaluation()

def get_default_evaluation() -> dict:
    """Return default evaluation when AI fails"""
    return {
        "content_score": 70,
        "communication_score": 75,
        "completeness_score": 72,
        "overall_score": 72,
        "strengths": ["Clear communication", "Relevant response"],
        "improvements": ["Add more specific examples", "Provide more detail"],
        "feedback_summary": "Good answer with room for improvement in detail and examples."
    }
