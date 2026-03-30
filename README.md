# Face Recognition System

Django-based face recognition system with YOLO phone detection capabilities.

## Features
- Face recognition using OpenCV
- Phone detection using YOLOv8
- Real-time camera monitoring
- Django admin dashboard
- Detection history tracking

## Requirements
- Python 3.8+
- Webcam
- Windows OS (for .bat scripts)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/bhargv/face-recognition-system.git
cd face-recognition-system
```

### 2. Install Dependencies
```bash
pip install django opencv-python opencv-contrib-python pillow ultralytics torch torchvision
```

### 3. Download Required Models
The YOLOv8 model will be downloaded automatically on first run, or you can download manually:
```bash
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

### 4. Run Setup
```bash
setup.bat
```

This will:
- Run database migrations
- Create admin user (username: `admin`, password: `admin`)
- Collect static files

## Usage

### Start the System

**Option 1: Using batch file**
```bash
start_detection.bat
```

**Option 2: Manual start**

Terminal 1 - Start Django server:
```bash
python manage.py runserver
```

Terminal 2 - Start phone detection:
```bash
python phone_detection_django.py
```

### Access Points
- Admin Panel: http://localhost:8000/admin/
- Phone Detection Dashboard: http://localhost:8000/phone-detection/
- Login credentials: `admin` / `admin`

### Controls
- Press `q` to quit detection
- Press `s` to manually save current frame

## Project Structure
```
face_project/
├── recognition/          # Main app for face recognition
├── face_project/         # Django project settings
├── phone_detection_django.py  # Phone detection script
├── setup.bat            # Setup script
├── start_detection.bat  # Quick start script
└── manage.py           # Django management
```

## Training Face Recognition
To train the system with new faces, add images to the training dataset and run:
```bash
python recognition/train.py
```

## Troubleshooting

### Torch Issues
If you encounter PyTorch errors, run:
```bash
fix_torch.bat
```

### Camera Not Working
- Check if another application is using the camera
- Verify camera permissions in Windows settings
- Try changing camera index in the detection script

## Notes
- Model files (*.pt, *.yml, *.pkl) are excluded from git
- Database and media files are not tracked
- Change admin password after first login
