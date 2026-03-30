import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'face_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Delete existing admin user if exists
if User.objects.filter(username='admin').exists():
    User.objects.filter(username='admin').delete()
    print("Existing admin user deleted")

# Create new admin user
User.objects.create_superuser('admin', 'admin@example.com', 'admin')
print("Admin user created successfully!")
print("Username: admin")
print("Password: admin")
