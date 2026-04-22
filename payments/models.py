# payments/models.py

from django.db import models
from django.conf import settings
from bookings.models import Booking

class Payment(models.Model):
    PAYMENT_MODES = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('online', 'Online'),
        ('bank_transfer', 'Bank Transfer'),
    )
    
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODES)
    transaction_id = models.CharField(max_length=100, blank=True, help_text="For online/card transactions")
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments_received')
    remarks = models.TextField(blank=True)
    
    def __str__(self):
        return f"Payment #{self.id} - {self.booking}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update booking paid amount
        booking = self.booking
        total_paid = booking.payments.aggregate(total=models.Sum('amount'))['total'] or 0
        booking.paid_amount = total_paid
        booking.save(update_fields=['paid_amount'])