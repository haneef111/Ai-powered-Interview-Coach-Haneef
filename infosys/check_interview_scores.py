"""
Check actual scores stored in database for debugging
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from pymongo import MongoClient
from config import Config
from bson import ObjectId

print("=" * 70)
print("CHECKING INTERVIEW SCORES IN DATABASE")
print("=" * 70)

try:
    # Connect to MongoDB
    print("\nConnecting to MongoDB...")
    client = MongoClient(Config.MONGO_URI)
    db = client.interview_coach
    print("✅ Connected to database")
    
    # Get all interviews
    interviews = list(db.interviews.find().sort('created_at', -1).limit(5))
    
    if not interviews:
        print("\n❌ No interviews found in database")
        print("   Complete an interview first, then run this script")
    else:
        print(f"\n✅ Found {len(interviews)} recent interview(s)\n")
        
        for idx, interview in enumerate(interviews, 1):
            print("=" * 70)
            print(f"INTERVIEW #{idx}")
            print("=" * 70)
            print(f"ID: {interview['_id']}")
            print(f"Status: {interview.get('status', 'unknown')}")
            print(f"Created: {interview.get('created_at', 'unknown')}")
            
            # Check answers
            answers = interview.get('answers', [])
            print(f"\nAnswers: {len(answers)}")
            
            if answers:
                for ans_idx, answer in enumerate(answers, 1):
                    print(f"\n  Answer {ans_idx}:")
                    print(f"    Question ID: {answer.get('question_id')}")
                    print(f"    Video Path: {answer.get('video_path', 'N/A')}")
                    print(f"    Analyzed: {answer.get('analyzed', False)}")
                    
                    # Check if video file exists
                    video_path = answer.get('video_path')
                    if video_path and os.path.exists(video_path):
                        size = os.path.getsize(video_path)
                        print(f"    Video File: ✅ Exists ({size:,} bytes)")
                    elif video_path:
                        print(f"    Video File: ❌ NOT FOUND")
                    
                    # Check analysis results
                    analysis = answer.get('analysis', {})
                    if analysis:
                        speech = analysis.get('speech_analysis', {})
                        facial = analysis.get('facial_analysis', {})
                        content = analysis.get('content_analysis', {})
                        
                        print(f"    Scores:")
                        print(f"      Speech: {speech.get('clarity_score', 0)}")
                        print(f"      Facial: {facial.get('confidence_score', 0)}")
                        print(f"      Content: {content.get('relevance_score', 0)}")
                        print(f"      Question: {analysis.get('question_score', 0)}")
                        
                        # Check transcript
                        transcript = speech.get('transcript', '')
                        if transcript:
                            print(f"      Transcript: {transcript[:80]}...")
                        else:
                            print(f"      Transcript: ❌ EMPTY")
            
            # Check overall feedback
            feedback = interview.get('feedback', {})
            if feedback:
                print(f"\nOverall Feedback:")
                print(f"  Overall Score: {feedback.get('overall_score', 0)}")
                avg_scores = feedback.get('average_scores', {})
                if avg_scores:
                    print(f"  Average Speech: {avg_scores.get('speech', 0)}")
                    print(f"  Average Facial: {avg_scores.get('facial', 0)}")
                    print(f"  Average Content: {avg_scores.get('content', 0)}")
            
            print()
    
    print("=" * 70)
    print("DIAGNOSIS")
    print("=" * 70)
    
    # Analyze the data
    has_zero_scores = False
    has_missing_videos = False
    has_empty_transcripts = False
    
    for interview in interviews:
        answers = interview.get('answers', [])
        for answer in answers:
            analysis = answer.get('analysis', {})
            if analysis:
                speech_score = analysis.get('speech_analysis', {}).get('clarity_score', 0)
                facial_score = analysis.get('facial_analysis', {}).get('confidence_score', 0)
                
                if speech_score == 0:
                    has_zero_scores = True
                if facial_score == 0:
                    has_zero_scores = True
                
                transcript = analysis.get('speech_analysis', {}).get('transcript', '')
                if not transcript or len(transcript) < 10:
                    has_empty_transcripts = True
            
            video_path = answer.get('video_path')
            if video_path and not os.path.exists(video_path):
                has_missing_videos = True
    
    if has_zero_scores:
        print("\n❌ ZERO SCORES DETECTED")
        print("\nLikely causes:")
        print("  1. FFmpeg not installed (most common)")
        print("  2. Video files cannot be processed")
        print("  3. Analysis services failing")
        print("\nFix:")
        print("  1. Run: check_ffmpeg.bat")
        print("  2. Install FFmpeg if missing")
        print("  3. Run: fix_dependencies.bat")
        print("  4. Restart backend")
        print("  5. Complete NEW interview")
    
    if has_missing_videos:
        print("\n❌ MISSING VIDEO FILES")
        print("  Some video files referenced in database don't exist")
        print("  This could cause analysis to fail")
    
    if has_empty_transcripts:
        print("\n❌ EMPTY TRANSCRIPTS")
        print("  Whisper failed to transcribe audio")
        print("  This means FFmpeg is likely missing")
        print("  Install FFmpeg and try again")
    
    if not has_zero_scores and not has_missing_videos and not has_empty_transcripts:
        print("\n✅ DATA LOOKS GOOD")
        print("  Scores are non-zero")
        print("  Video files exist")
        print("  Transcripts are present")
        print("\n  If you're still seeing 0 on frontend:")
        print("    1. Clear browser cache")
        print("    2. Logout and login again")
        print("    3. Check browser console (F12)")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    print("\nMake sure:")
    print("  1. MongoDB is accessible")
    print("  2. Config.py has correct MONGO_URI")
    print("  3. Internet connection is working")

print("\n" + "=" * 70)
