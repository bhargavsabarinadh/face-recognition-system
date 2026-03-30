from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_person, name='add_person'),
    path('train/', views.train_faces, name='train_faces'),
    path('recognize/', views.recognize, name='recognize'),
    path('phone-detection/', views.phone_detection_dashboard, name='phone_detection_dashboard'),
]