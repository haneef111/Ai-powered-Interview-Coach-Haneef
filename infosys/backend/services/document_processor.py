"""
Document Processing Service
Extracts text and analyzes resume and job descriptions
"""
import PyPDF2
import docx
import re
from typing import Dict, List

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file"""
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text.strip()
    except Exception as e:
        print(f"PDF extraction error: {e}")
        return ""

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    except Exception as e:
        print(f"DOCX extraction error: {e}")
        return ""

def extract_text_from_txt(file_path: str) -> str:
    """Extract text from TXT file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except Exception as e:
        print(f"TXT extraction error: {e}")
        return ""

def extract_text(file_path: str) -> str:
    """Extract text based on file extension"""
    if file_path.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.lower().endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.lower().endswith('.txt'):
        return extract_text_from_txt(file_path)
    else:
        return ""

def extract_skills(text: str) -> List[str]:
    """Extract skills from text using keyword matching"""
    # Common technical skills
    skill_keywords = [
        'python', 'java', 'javascript', 'react', 'node', 'angular', 'vue',
        'sql', 'mongodb', 'postgresql', 'mysql', 'aws', 'azure', 'docker',
        'kubernetes', 'git', 'agile', 'scrum', 'machine learning', 'ai',
        'data analysis', 'leadership', 'communication', 'problem solving',
        'teamwork', 'project management', 'html', 'css', 'typescript',
        'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'flutter', 'django',
        'flask', 'spring', 'express', 'rest api', 'graphql', 'microservices'
    ]
    
    text_lower = text.lower()
    found_skills = []
    
    for skill in skill_keywords:
        if skill in text_lower:
            found_skills.append(skill.title())
    
    return list(set(found_skills))  # Remove duplicates

def extract_experience_years(text: str) -> int:
    """Extract years of experience from text"""
    patterns = [
        r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
        r'experience\s*:\s*(\d+)\+?\s*years?',
        r'(\d+)\+?\s*yrs?\s+(?:of\s+)?experience'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return int(match.group(1))
    
    return 0

def analyze_document(text: str, doc_type: str = 'resume') -> Dict:
    """Analyze document and extract key information"""
    skills = extract_skills(text)
    experience_years = extract_experience_years(text)
    
    # Extract education keywords
    education_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college']
    has_education = any(keyword in text.lower() for keyword in education_keywords)
    
    return {
        'skills': skills,
        'experience_years': experience_years,
        'has_education': has_education,
        'word_count': len(text.split()),
        'text_preview': text[:500] if len(text) > 500 else text
    }
