"""
Question Generation Service using Google Gemini AI
Generates personalized interview questions based on resume and job description
"""
from typing import List, Dict
import google.generativeai as genai
from config import Config
import json

# Configure Gemini API
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-lite')  # Correct model name

def generate_questions_from_analysis(resume_analysis: Dict, job_analysis: Dict) -> List[Dict]:
    """Generate 10 personalized interview questions using Gemini AI"""
    
    try:
        # Prepare context for Gemini
        resume_skills = resume_analysis.get('skills', [])
        resume_experience = resume_analysis.get('experience_years', 0)
        job_skills = job_analysis.get('skills', [])
        resume_preview = resume_analysis.get('text_preview', '')
        job_description = job_analysis.get('text_preview', '')
        
        # Create prompt for Gemini
        prompt = f"""You are an expert interview coach. Generate exactly 10 personalized interview questions based on the candidate's resume and the job description.

CANDIDATE RESUME SUMMARY:
- Skills: {', '.join(resume_skills) if resume_skills else 'Not specified'}
- Years of Experience: {resume_experience}
- Resume Preview: {resume_preview[:500]}

JOB DESCRIPTION:
- Required Skills: {', '.join(job_skills) if job_skills else 'Not specified'}
- Job Details: {job_description[:500]}

REQUIREMENTS:
1. Generate EXACTLY 10 questions
2. Mix of behavioral, technical, and situational questions
3. Questions should be relevant to the candidate's experience level
4. Include questions about skills mentioned in both resume and job description
5. Include questions about any skill gaps
6. Questions should be clear, professional, and interview-appropriate
7. Each question should be unique and meaningful

Return the questions in this EXACT JSON format:
[
  {{"id": 1, "question": "Question text here", "type": "behavioral", "category": "introduction"}},
  {{"id": 2, "question": "Question text here", "type": "technical", "category": "skills"}},
  ...
]

Valid types: behavioral, technical, situational
Valid categories: introduction, experience, skills, problem_solving, teamwork, motivation, career_goals, learning_ability

Generate the 10 questions now:"""

        # Call Gemini API
        print("Calling Gemini AI to generate questions...")
        response = model.generate_content(prompt)
        
        # Parse response
        response_text = response.text.strip()
        
        # Extract JSON from response (handle markdown code blocks)
        if '```json' in response_text:
            json_start = response_text.find('```json') + 7
            json_end = response_text.find('```', json_start)
            response_text = response_text[json_start:json_end].strip()
        elif '```' in response_text:
            json_start = response_text.find('```') + 3
            json_end = response_text.find('```', json_start)
            response_text = response_text[json_start:json_end].strip()
        
        # Parse JSON
        questions = json.loads(response_text)
        
        # Validate and ensure exactly 10 questions
        if not isinstance(questions, list):
            raise ValueError("Response is not a list")
        
        # Ensure we have exactly 10 questions
        if len(questions) < 10:
            # Add default questions to reach 10
            default_questions = generate_default_questions()
            questions.extend(default_questions[len(questions):10])
        elif len(questions) > 10:
            questions = questions[:10]
        
        # Ensure all questions have required fields
        for i, q in enumerate(questions):
            if 'id' not in q:
                q['id'] = i + 1
            if 'type' not in q:
                q['type'] = 'behavioral'
            if 'category' not in q:
                q['category'] = 'general'
        
        print(f"Successfully generated {len(questions)} questions using Gemini AI")
        return questions
        
    except Exception as e:
        print(f"Error generating questions with Gemini: {e}")
        print("Falling back to default questions")
        return generate_default_questions()

def generate_default_questions() -> List[Dict]:
    """Generate 10 default questions when AI generation fails"""
    return [
        {
            'id': 1,
            'question': 'Tell me about yourself and your professional background.',
            'type': 'behavioral',
            'category': 'introduction'
        },
        {
            'id': 2,
            'question': 'What are your greatest strengths and how do they apply to this role?',
            'type': 'behavioral',
            'category': 'strengths'
        },
        {
            'id': 3,
            'question': 'Describe a challenging project you worked on and how you overcame obstacles.',
            'type': 'behavioral',
            'category': 'problem_solving'
        },
        {
            'id': 4,
            'question': 'How do you stay updated with the latest technologies and industry trends?',
            'type': 'technical',
            'category': 'learning_ability'
        },
        {
            'id': 5,
            'question': 'Tell me about a time when you had to work with a difficult team member.',
            'type': 'behavioral',
            'category': 'teamwork'
        },
        {
            'id': 6,
            'question': 'Why are you interested in this position and our company?',
            'type': 'behavioral',
            'category': 'motivation'
        },
        {
            'id': 7,
            'question': 'Describe a situation where you had to learn a new technology quickly.',
            'type': 'situational',
            'category': 'learning_ability'
        },
        {
            'id': 8,
            'question': 'How do you prioritize tasks when working on multiple projects?',
            'type': 'behavioral',
            'category': 'time_management'
        },
        {
            'id': 9,
            'question': 'What is your biggest professional achievement and why?',
            'type': 'behavioral',
            'category': 'achievements'
        },
        {
            'id': 10,
            'question': 'Where do you see yourself in 3-5 years?',
            'type': 'behavioral',
            'category': 'career_goals'
        }
    ]
