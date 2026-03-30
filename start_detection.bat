@echo off
echo ========================================
echo Phone Detection System - Quick Start
echo ========================================
echo.

cd "C:\Users\Lenovo\Desktop\tts\FACE RECOGNITION\FACE RECOGUNATION\face_project"

echo Checking YOLOv8 model...
if exist yolov8n.pt (
    echo [OK] YOLOv8 model found
) else (
    echo [INFO] Downloading YOLOv8 model...
    python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
)

echo.
echo Starting Phone Detection System...
echo.
echo Controls:
echo - Press 'q' to quit
echo - Press 's' to manually save current frame
echo.
echo ========================================
echo.

python phone_detection_django.py

pause
