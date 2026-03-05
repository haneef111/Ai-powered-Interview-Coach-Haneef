"""
Comprehensive diagnostic for zero scores issue
Run this to find out exactly why speech and facial scores are 0
"""
import sys
import os
import subprocess

print("=" * 70)
print("DIAGNOSING ZERO SCORES ISSUE")
print("=" * 70)

issues_found = []
fixes_needed = []

# Check 1: FFmpeg
print("\n[1/6] Checking FFmpeg installation...")
try:
    result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        print("✅ FFmpeg is installed")
        version_line = result.stdout.split('\n')[0]
        print(f"    Version: {version_line}")
    else:
        print("❌ FFmpeg command failed")
        issues_found.append("FFmpeg installed but not working")
        fixes_needed.append("Reinstall FFmpeg")
except FileNotFoundError:
    print("❌ FFmpeg is NOT installed")
    issues_found.append("FFmpeg is missing (CRITICAL)")
    fixes_needed.append("Install FFmpeg: Run install_ffmpeg_guide.bat or choco install ffmpeg")
except Exception as e:
    print(f"❌ FFmpeg check failed: {e}")
    issues_found.append("FFmpeg check error")

# Check 2: Python packages
print("\n[2/6] Checking Python packages...")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

packages = {
    'whisper': 'openai-whisper',
    'cv2': 'opencv-python',
    'mediapipe': 'mediapipe',
    'google.generativeai': 'google-generativeai',
    'ffmpeg': 'ffmpeg-python'
}

missing_packages = []
for module_name, package_name in packages.items():
    try:
        if module_name == 'cv2':
            import cv2
            print(f"✅ {package_name} installed (v{cv2.__version__})")
        elif module_name == 'mediapipe':
            import mediapipe as mp
            print(f"✅ {package_name} installed (v{mp.__version__})")
            try:
                mp.solutions.face_mesh
                print("   ✅ face_mesh accessible")
            except AttributeError:
                print("   ❌ face_mesh NOT accessible")
                issues_found.append("MediaPipe face_mesh not accessible")
                fixes_needed.append("Run: pip install mediapipe==0.10.9")
        elif module_name == 'whisper':
            import whisper
            print(f"✅ {package_name} installed")
        elif module_name == 'google.generativeai':
            import google.generativeai as genai
            print(f"✅ {package_name} installed")
        elif module_name == 'ffmpeg':
            import ffmpeg
            print(f"✅ {package_name} installed")
    except ImportError:
        print(f"❌ {package_name} NOT installed")
        missing_packages.append(package_name)
        issues_found.append(f"{package_name} missing")

if missing_packages:
    fixes_needed.append(f"Run: pip install {' '.join(missing_packages)}")

# Check 3: Uploads folder
print("\n[3/6] Checking uploads folder...")
uploads_path = os.path.join('backend', 'uploads')
if os.path.exists(uploads_path):
    files = [f for f in os.listdir(uploads_path) if f.endswith(('.webm', '.mp4', '.avi'))]
    print(f"✅ Uploads folder exists")
    print(f"   Video files: {len(files)}")
    
    if len(files) == 0:
        print("   ⚠️  No video files found")
        print("   This is normal if you haven't completed an interview yet")
    else:
        print(f"   Sample: {files[0]}")
        test_video = os.path.join(uploads_path, files[0])
        
        # Check 4: Test video file access
        print("\n[4/6] Testing video file access...")
        try:
            file_size = os.path.getsize(test_video)
            print(f"✅ Can read video file")
            print(f"   Size: {file_size:,} bytes")
            
            if file_size < 1000:
                print("   ⚠️  File is very small, might be corrupted")
                issues_found.append("Video file too small")
        except Exception as e:
            print(f"❌ Cannot read video file: {e}")
            issues_found.append("Video file access error")
        
        # Check 5: Test OpenCV can open video
        print("\n[5/6] Testing OpenCV video reading...")
        try:
            import cv2
            cap = cv2.VideoCapture(test_video)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    print("✅ OpenCV can read video")
                    print(f"   Frame size: {frame.shape}")
                else:
                    print("❌ OpenCV cannot read frames")
                    issues_found.append("OpenCV cannot decode video")
                    fixes_needed.append("Install FFmpeg or change video format to MP4")
                cap.release()
            else:
                print("❌ OpenCV cannot open video file")
                issues_found.append("OpenCV cannot open WebM (codec issue)")
                fixes_needed.append("Install FFmpeg with VP8/VP9 codec support")
        except Exception as e:
            print(f"❌ OpenCV test failed: {e}")
            issues_found.append(f"OpenCV error: {e}")
        
        # Check 6: Test Whisper transcription
        print("\n[6/6] Testing Whisper transcription...")
        try:
            import whisper
            print("   Loading Whisper model (this may take a minute)...")
            model = whisper.load_model("base")
            print("   Transcribing (this may take 30-60 seconds)...")
            result = model.transcribe(test_video, fp16=False)
            transcript = result['text']
            if transcript and len(transcript) > 5:
                print(f"✅ Whisper transcription works")
                print(f"   Transcript: {transcript[:100]}...")
            else:
                print("❌ Whisper returned empty transcript")
                issues_found.append("Whisper transcription empty")
                fixes_needed.append("Check if video has audio track")
        except Exception as e:
            print(f"❌ Whisper test failed: {e}")
            issues_found.append(f"Whisper error: {e}")
            if "ffmpeg" in str(e).lower():
                fixes_needed.append("Install FFmpeg (CRITICAL)")
else:
    print(f"❌ Uploads folder not found")
    print("   This is normal if you haven't completed an interview yet")

# Summary
print("\n" + "=" * 70)
print("DIAGNOSIS SUMMARY")
print("=" * 70)

if not issues_found:
    print("\n✅ NO ISSUES FOUND!")
    print("\nYour system should be working correctly.")
    print("If you're still getting 0 scores:")
    print("  1. Complete a new interview")
    print("  2. Check backend logs during analysis")
    print("  3. Verify you're speaking during recording")
else:
    print(f"\n❌ FOUND {len(issues_found)} ISSUE(S):\n")
    for i, issue in enumerate(issues_found, 1):
        print(f"  {i}. {issue}")
    
    print(f"\n🔧 FIXES NEEDED:\n")
    for i, fix in enumerate(fixes_needed, 1):
        print(f"  {i}. {fix}")

print("\n" + "=" * 70)
print("RECOMMENDED ACTIONS")
print("=" * 70)

if any("FFmpeg" in issue for issue in issues_found):
    print("""
🚨 CRITICAL: Install FFmpeg first!

Run one of these:
  1. check_ffmpeg.bat          (Check if installed)
  2. install_ffmpeg_guide.bat  (Installation guide)
  3. choco install ffmpeg      (If you have Chocolatey)

After installing FFmpeg:
  1. CLOSE and REOPEN your terminal/IDE
  2. Run: fix_dependencies.bat
  3. Run: python backend/app.py
  4. Test with a new interview
""")
else:
    print("""
Run these commands:
  1. fix_dependencies.bat      (Fix Python packages)
  2. python backend/app.py     (Restart backend)
  3. Complete a test interview (Check if scores work)
""")

print("=" * 70)
print("\nFor detailed instructions, see: ZERO_SCORES_FIX.md")
print("=" * 70)
