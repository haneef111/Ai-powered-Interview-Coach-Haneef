"""
Check if your system can process WebM video files
"""
import cv2
import sys

print("=" * 60)
print("VIDEO CODEC SUPPORT CHECK")
print("=" * 60)

# Check OpenCV build info
print(f"\nOpenCV Version: {cv2.__version__}")
print(f"OpenCV Build Info:")
print(f"  - Video I/O: {cv2.getBuildInformation()}")

# Test video codecs
print("\n" + "=" * 60)
print("TESTING VIDEO CODECS")
print("=" * 60)

codecs_to_test = [
    ('VP8', cv2.VideoWriter_fourcc(*'VP80')),
    ('VP9', cv2.VideoWriter_fourcc(*'VP90')),
    ('H264', cv2.VideoWriter_fourcc(*'H264')),
    ('MJPEG', cv2.VideoWriter_fourcc(*'MJPG')),
]

for codec_name, fourcc in codecs_to_test:
    try:
        # Try to create a test writer
        test_writer = cv2.VideoWriter('test_temp.avi', fourcc, 20.0, (640, 480))
        if test_writer.isOpened():
            print(f"✓ {codec_name} codec supported")
            test_writer.release()
        else:
            print(f"✗ {codec_name} codec NOT supported")
    except Exception as e:
        print(f"✗ {codec_name} codec error: {e}")

# Clean up test file
import os
if os.path.exists('test_temp.avi'):
    os.remove('test_temp.avi')

print("\n" + "=" * 60)
print("RECOMMENDATIONS")
print("=" * 60)
print("""
If VP8/VP9 codecs are not supported, you need to:

OPTION 1 - Install FFmpeg (RECOMMENDED):
  1. Download from: https://www.gyan.dev/ffmpeg/builds/
  2. Extract and add to PATH
  3. Restart your terminal/IDE

OPTION 2 - Use opencv-python-headless with FFmpeg:
  pip uninstall opencv-python
  pip install opencv-python-headless

OPTION 3 - Convert WebM to MP4 in frontend:
  Change MediaRecorder mimeType from 'video/webm' to 'video/mp4'
  (Note: Not all browsers support MP4 recording)
""")
print("=" * 60)
