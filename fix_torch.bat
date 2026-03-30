@echo off
echo ========================================
echo Fixing Torch/Torchvision Compatibility
echo ========================================
echo.

cd "C:\Users\Lenovo\Desktop\tts\FACE RECOGNITION\FACE RECOGUNATION\face_project"

echo [1/2] Uninstalling incompatible versions...
pip uninstall torch torchvision -y

echo.
echo [2/2] Installing compatible versions...
pip install torch==2.6.0 torchvision==0.21.0

echo.
echo ========================================
echo Fix Complete!
echo ========================================
echo.
echo Now you can run:
echo python phone_detection_django_fixed.py
echo.
pause
