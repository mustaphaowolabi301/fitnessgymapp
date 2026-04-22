# trainers/models.py

from django.db import models
from django.conf import settings

class Trainer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trainer_profile')
    bio = models.TextField()
    specialties = models.CharField(max_length=255, help_text="Comma-separated list")
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    photo = models.ImageField(upload_to='trainers/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Trainer: {self.user.get_full_name()}"