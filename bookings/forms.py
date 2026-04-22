# bookings/forms.py

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

class BookingForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Start Date'
    )
    payment_method = forms.ChoiceField(
        choices=[('offline', 'Pay at Gym'), ('online', 'Pay Online (Coming Soon)')],
        widget=forms.RadioSelect,
        initial='offline'
    )
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}), required=False)
    
    def __init__(self, *args, **kwargs):
        self.package = kwargs.pop('package')
        super().__init__(*args, **kwargs)
    
    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        if start_date < timezone.now().date():
            raise ValidationError("Start date cannot be in the past.")
        return start_date