@echo off
echo ========================================
echo Phone Detection System Setup
echo ========================================
echo.

cd "C:\Users\Lenovo\Desktop\tts\FACE RECOGNITION\FACE RECOGUNATION\face_project"

echo [1/5] Running migrations...
python manage.py makemigrations
python manage.py migrate

echo.
echo [2/5] Creating admin user (username: admin, password: admin)...
python create_admin.py

echo.
echo [3/5] Collecting static files...
python manage.py collectstatic --noinput

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the system:
echo 1. Run Django server: python manage.py runserver
echo 2. Run detection (in new terminal): python phone_detection_django.py
echo.
echo Access points:
echo - Admin Panel: http://localhost:8000/admin/
echo - Phone Detection Dashboard: http://localhost:8000/phone-detection/
echo - Login: admin / admin
echo.
pause
