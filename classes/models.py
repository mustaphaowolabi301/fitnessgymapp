# classes/models.py

from django.db import models
from django.conf import settings
from trainers.models import Trainer

class ClassSchedule(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    trainer = models.ForeignKey(Trainer, on_delete=models.PROTECT, related_name='classes')
    capacity = models.PositiveIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_recurring = models.BooleanField(default=False)
    recurrence_pattern = models.CharField(max_length=50, blank=True, help_text="e.g., 'Weekly on Monday'")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} with {self.trainer.user.get_full_name()} at {self.start_time}"
    
    def available_spots(self):
        booked = self.bookings.filter(status='booked').count()
        return self.capacity - booked

class ClassBooking(models.Model):
    STATUS_CHOICES = (
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('attended', 'Attended'),
    )
    
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='class_bookings')
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name='bookings')
    booked_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='booked')
    
    class Meta:
        unique_together = ('member', 'class_schedule')  # Prevent double booking
    
    def __str__(self):
        return f"{self.member.email} - {self.class_schedule.name}"