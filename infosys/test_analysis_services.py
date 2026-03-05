"""
Test script for speech and facial analysis services
Run this to verify that analysis services are working correctly
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("=" * 60)
print("TESTING ANALYSIS SERVICES")
print("=" * 60)

# Test 1: Check if required packages are installed
print("\n1. Checking required packages...")
try:
    import whisper
    print("✓ Whisper installed")
except ImportError as e:
    print(f"✗ Whisper NOT installed: {e}")

try:
    import cv2
    print(f"✓ OpenCV installed (version: {cv2.__version__})")
except ImportError as e:
    print(f"✗ OpenCV NOT installed: {e}")

try:
    import mediapipe as mp
    print(f"✓ MediaPipe installed (version: {mp.__version__})")
    try:
        mp_face_mesh = mp.solutions.face_mesh
        print("✓ MediaPipe face_mesh accessible")
    except AttributeError as e:
        print(f"✗ MediaPipe face_mesh NOT accessible: {e}")
except ImportError as e:
    print(f"✗ MediaPipe NOT installed: {e}")

try:
    import google.generativeai as genai
    print("✓ Google Generative AI installed")
except ImportError as e:
    print(f"✗ Google Generative AI NOT installed: {e}")

# Test 2: Check Gemini API
print("\n2. Testing Gemini API connection...")
try:
    from config import Config
    import google.generativeai as genai
    
    genai.configure(api_key=Config.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    response = model.generate_content("Say 'Hello' in one word")
    print(f"✓ Gemini API working: {response.text[:50]}")
except Exception as e:
    print(f"✗ Gemini API error: {e}")

# Test 3: Check uploads folder
print("\n3. Checking uploads folder...")
uploads_path = os.path.join('backend', 'uploads')
if os.path.exists(uploads_path):
    files = os.listdir(uploads_path)
    print(f"✓ Uploads folder exists")
    print(f"  Files in uploads: {len(files)}")
    if files:
        print(f"  Sample files: {files[:3]}")
        
        # Test analysis on first video file
        video_file = None
        for f in files:
            if f.endswith(('.webm', '.mp4', '.avi')):
                video_file = os.path.join(uploads_path, f)
                break
        
        if video_file:
            print(f"\n4. Testing analysis on: {os.path.basename(video_file)}")
            
            # Test speech analysis
            print("\n  Testing speech analysis...")
            try:
                from services.speech_analysis import analyze_speech
                speech_result = analyze_speech(video_file)
                print(f"  ✓ Speech Score: {speech_result.get('clarity_score', 0)}")
                print(f"    Transcript: {speech_result.get('transcript', '')[:100]}...")
            except Exception as e:
                print(f"  ✗ Speech analysis failed: {e}")
            
            # Test facial analysis
            print("\n  Testing facial analysis...")
            try:
                from services.facial_analysis import analyze_facial_expressions
                facial_result = analyze_facial_expressions(video_file)
                print(f"  ✓ Facial Score: {facial_result.get('confidence_score', 0)}")
                print(f"    Eye contact: {facial_result.get('eye_contact_percentage', 0)}%")
            except Exception as e:
                print(f"  ✗ Facial analysis failed: {e}")
    else:
        print(f"  No video files found in uploads folder")
else:
    print(f"✗ Uploads folder not found at {uploads_path}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
print("\nNEXT STEPS:")
print("1. If packages are missing, run: pip install -r backend/requirements.txt")
print("2. If no video files exist, complete an interview to generate test data")
print("3. If analysis fails, check the error messages above")
print("=" * 60)
