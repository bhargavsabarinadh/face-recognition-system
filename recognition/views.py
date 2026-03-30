import os
import cv2
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Person, PhoneUsageDetection

def add_person(request):
    if request.method == 'POST':
        name = request.POST['name']
        person = Person.objects.create(name=name)

        save_path = os.path.join(settings.MEDIA_ROOT, 'faces', name)
        os.makedirs(save_path, exist_ok=True)

        from .camera import capture_faces
        capture_faces(save_path)
        return redirect('add_person')

    return render(request, 'add_person.html', {
        'title': 'Add New Person',
        'subtitle': 'Register a new face for recognition'
    })

def train_faces(request):
    from .train import train_model
    train_model()
    return render(request, 'train.html', {
        'title': 'Train Faces',
        'subtitle': 'Model training & optimization',
        'status': 'completed',
        'persons_count': Person.objects.count()
    })

def recognize(request):
    from .recognize import recognize_face
    recognize_face()
    return render(request, 'recognize.html', {
        'title': 'Live Recognition',
        'subtitle': 'Real-time face identification'
    })

@login_required
def phone_detection_dashboard(request):
    """Dashboard showing phone usage detections"""
    detections = PhoneUsageDetection.objects.all()[:50]  # Latest 50 detections

    stats = {
        'total_detections': PhoneUsageDetection.objects.count(),
        'today_detections': PhoneUsageDetection.objects.filter(
            detected_at__date=timezone.now().date()
        ).count(),
        'total_phone_users': sum(d.phone_users_count for d in PhoneUsageDetection.objects.all()),
    }

    return render(request, 'phone_detection_dashboard.html', {
        'detections': detections,
        'stats': stats,
        'title': 'Phone Detection Dashboard',
    })

from django.utils import timezone
