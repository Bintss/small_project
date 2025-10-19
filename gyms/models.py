# gyms/models.py
from django.db import models
from django.conf import settings

class Gym(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gyms')
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Court(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='courts')
    name = models.CharField(max_length=50) # e.g., "1번 코트", "A 코트"
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.gym.name} - {self.name}'