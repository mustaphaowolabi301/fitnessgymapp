from django.db import models
from django.conf import settings

class EmailCampaign(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    recipient_count = models.PositiveIntegerField(default=0)
    sent_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    filter_criteria = models.JSONField(default=dict, blank=True)  # store filter params used
    
    def __str__(self):
        return f"{self.subject} - {self.sent_at.strftime('%Y-%m-%d %H:%M')}"