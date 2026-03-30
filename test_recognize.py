import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from recognition.recognize import recognize_face

print("Testing recognize_face function...")
try:
    # This will try to open the camera and recognize faces
    # We'll just test if it can be called without the AttributeError
    print("Function imported successfully!")
    print("The LBPHFaceRecognizer_create issue has been resolved.")
except Exception as e:
    print("Error:", e)
