from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Inquiry
from .forms import InquiryForm
from packages.models import MembershipPackage
from trainers.models import Trainer


def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def trainers_list(request):
    trainers = Trainer.objects.filter(is_active=True).select_related('user')
    return render(request, 'core/trainers.html', {'trainers': trainers})

def equipment(request):
    return render(request, 'core/equipment.html')

def membership_plans(request):
    # Will fetch from packages app later
    return render(request, 'core/membership_plans.html')

def contact(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your inquiry has been sent. We will get back to you soon.')
            return redirect('core:contact')
    else:
        form = InquiryForm()
    return render(request, 'core/contact.html', {'form': form})

def home(request):
    featured_packages = MembershipPackage.objects.filter(is_active=True)[:3]
    return render(request, 'core/home.html', {'featured_packages': featured_packages})

def membership_plans(request):
    packages = MembershipPackage.objects.filter(is_active=True)
    return render(request, 'core/membership_plans.html', {'packages': packages})