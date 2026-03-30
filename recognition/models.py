from django.db import models
from django.utils import timezone

class Person(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class PhoneUsageDetection(models.Model):
    image = models.ImageField(upload_to='phone_detections/')
    detected_at = models.DateTimeField(default=timezone.now)
    person_count = models.IntegerField(default=0)
    phone_count = models.IntegerField(default=0)
    phone_users_count = models.IntegerField(default=0)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-detected_at']
        verbose_name = 'Phone Usage Detection'
        verbose_name_plural = 'Phone Usage Detections'

    def __str__(self):
        return f"Detection at {self.detected_at.strftime('%Y-%m-%d %H:%M:%S')} - {self.phone_users_count} user(s)"