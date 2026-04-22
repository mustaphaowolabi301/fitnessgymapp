# bookings/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from packages.models import MembershipPackage
from .models import Booking
from payments.models import Payment
from .forms import BookingForm

@login_required
def apply_package(request, package_id):
    package = get_object_or_404(MembershipPackage, id=package_id, is_active=True)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, package=package)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = start_date + timedelta(days=package.duration_days)
            
            booking = Booking.objects.create(
                member=request.user,
                package=package,
                start_date=start_date,
                end_date=end_date,
                total_amount=package.price,
                status='pending'
            )
            
            # If offline payment selected, show message
            messages.success(request, 'Your booking has been created. Please make payment at the gym reception.')
            return redirect('bookings:history')
    else:
        form = BookingForm(package=package)
    
    return render(request, 'bookings/apply.html', {'package': package, 'form': form})

@login_required
def booking_history(request):
    bookings = Booking.objects.filter(member=request.user).order_by('-created_at')
    return render(request, 'bookings/history.html', {'bookings': bookings})

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, member=request.user)
    payments = booking.payments.all()
    return render(request, 'bookings/detail.html', {'booking': booking, 'payments': payments})

# Add to bookings/views.py
@login_required
def make_payment(request, booking_id):
    # Placeholder for online payment integration
    messages.info(request, "Online payment coming soon. Please pay at the gym.")
    return redirect('bookings:detail', booking_id=booking_id)