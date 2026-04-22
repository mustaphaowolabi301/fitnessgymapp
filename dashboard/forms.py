from payments.models import Payment
from bookings.models import Booking
from django import forms
from packages.models import PackageCategory, PackageType, MembershipPackage
from classes.models import ClassSchedule

class PackageCategoryForm(forms.ModelForm):
    class Meta:
        model = PackageCategory
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PackageTypeForm(forms.ModelForm):
    class Meta:
        model = PackageType
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MembershipPackageForm(forms.ModelForm):
    class Meta:
        model = MembershipPackage
        fields = ['name', 'category', 'package_type', 'duration_days', 'price', 'features', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'package_type': forms.Select(attrs={'class': 'form-select'}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'features': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter one feature per line'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_features(self):
        features = self.cleaned_data['features']
        # Convert newline-separated to lines for template display later
        return features

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_mode', 'transaction_id', 'remarks']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'payment_mode': forms.Select(attrs={'class': 'form-select'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class BookingStatusForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
from trainers.models import Trainer

class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['user', 'bio', 'specialties', 'hourly_rate', 'photo', 'is_active']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'specialties': forms.TextInput(attrs={'class': 'form-control'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
class ClassScheduleForm(forms.ModelForm):
    class Meta:
        model = ClassSchedule
        fields = ['name', 'description', 'trainer', 'capacity', 'start_time', 'end_time', 'is_recurring', 'recurrence_pattern', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'trainer': forms.Select(attrs={'class': 'form-select'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_recurring': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'recurrence_pattern': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
class POSLookupForm(forms.Form):
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}))
    phone = forms.CharField(required=False, max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}))
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')
        if not email and not phone:
            raise forms.ValidationError("Please provide either email or phone.")
        return cleaned_data

class POSPackageSelectForm(forms.Form):
    package = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select'}))
    
    def __init__(self, *args, **kwargs):
        packages = kwargs.pop('packages')
        super().__init__(*args, **kwargs)
        self.fields['package'].choices = [(p.id, f"{p.name} - ${p.price} ({p.duration_days} days)") for p in packages]

class POSPaymentForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    payment_mode = forms.ChoiceField(choices=Payment.PAYMENT_MODES, widget=forms.Select(attrs={'class': 'form-select'}))
    transaction_id = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional'}))
    remarks = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))
    
class EmailCampaignForm(forms.Form):
    FILTER_CHOICES = [
        ('all_active', 'All Active Members'),
        ('package', 'Specific Package'),
        ('pending_payment', 'Members with Pending Payments'),
        ('expiring_soon', 'Membership Expiring within 30 Days'),
    ]
    
    recipient_filter = forms.ChoiceField(choices=FILTER_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    package = forms.ModelChoiceField(queryset=MembershipPackage.objects.filter(is_active=True), required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    subject = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10}))
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('recipient_filter') == 'package' and not cleaned_data.get('package'):
            raise forms.ValidationError("Please select a package.")
        return cleaned_data