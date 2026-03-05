"""
Quick test script for Gemini AI integration
"""
import sys
sys.path.append('backend')

from services.question_generator import generate_questions_from_analysis, generate_default_questions
from services.gemini_evaluator import evaluate_answer_with_gemini

print("="*60)
print("TESTING GEMINI AI INTEGRATION")
print("="*60)

# Test 1: Question Generation
print("\n1. Testing Question Generation...")
print("-"*60)

resume_analysis = {
    'skills': ['Python', 'Django', 'React', 'PostgreSQL'],
    'experience_years': 3,
    'text_preview': 'Software Engineer with 3 years experience in web development using Python and React.'
}

job_analysis = {
    'skills': ['Python', 'AWS', 'Docker', 'Kubernetes'],
    'text_preview': 'Looking for a Backend Engineer with Python and cloud experience.'
}

try:
    questions = generate_questions_from_analysis(resume_analysis, job_analysis)
    print(f"✓ Generated {len(questions)} questions")
    print("\nSample questions:")
    for i, q in enumerate(questions[:3], 1):
        print(f"{i}. {q['question']}")
        print(f"   Type: {q['type']}, Category: {q['category']}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 2: Answer Evaluation
print("\n\n2. Testing Answer Evaluation...")
print("-"*60)

question = "Tell me about a challenging project you worked on."
answer = """I worked on a project to migrate our monolithic application to microservices. 
The main challenge was ensuring zero downtime during the migration. I led a team of 3 developers, 
and we used Docker and Kubernetes for containerization. We implemented a gradual rollout strategy, 
migrating one service at a time. The result was a 40% improvement in system performance and 
better scalability. It took 6 months to complete."""

try:
    evaluation = evaluate_answer_with_gemini(question, answer, 'behavioral')
    print(f"✓ Answer evaluated successfully")
    print(f"\nScores:")
    print(f"  Content: {evaluation['content_score']}/100")
    print(f"  Communication: {evaluation['communication_score']}/100")
    print(f"  Completeness: {evaluation['completeness_score']}/100")
    print(f"  Overall: {evaluation['overall_score']}/100")
    print(f"\nStrengths:")
    for s in evaluation['strengths']:
        print(f"  • {s}")
    print(f"\nImprovements:")
    for i in evaluation['improvements']:
        print(f"  • {i}")
    print(f"\nFeedback: {evaluation['feedback_summary']}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)
print("\nIf both tests passed, Gemini AI is working correctly!")
print("Now restart your backend: python backend/app.py")
