from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import ClassSchedule, ClassBooking

@login_required
def class_schedule(request):
    upcoming_classes = ClassSchedule.objects.filter(
        start_time__gte=timezone.now(),
        is_active=True
    ).select_related('trainer__user').order_by('start_time')
    
    # Get user's current bookings for these classes
    user_bookings = ClassBooking.objects.filter(
        member=request.user,
        status='booked'
    ).values_list('class_schedule_id', flat=True)
    
    return render(request, 'classes/schedule.html', {
        'classes': upcoming_classes,
        'user_bookings': user_bookings,
    })

@login_required
def book_class(request, class_id):
    class_obj = get_object_or_404(ClassSchedule, id=class_id, is_active=True)
    
    # Check if user already booked
    existing = ClassBooking.objects.filter(
        member=request.user,
        class_schedule=class_obj,
        status='booked'
    ).exists()
    if existing:
        messages.warning(request, 'You have already booked this class.')
        return redirect('classes:schedule')
    
    # Check availability
    if class_obj.available_spots() <= 0:
        messages.error(request, 'This class is fully booked.')
        return redirect('classes:schedule')
    
    ClassBooking.objects.create(
        member=request.user,
        class_schedule=class_obj,
        status='booked'
    )
    messages.success(request, f'You have successfully booked {class_obj.name}.')
    return redirect('classes:my_classes')

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(ClassBooking, id=booking_id, member=request.user)
    if booking.status == 'booked':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled.')
    else:
        messages.error(request, 'This booking cannot be cancelled.')
    return redirect('classes:my_classes')

@login_required
def my_classes(request):
    bookings = ClassBooking.objects.filter(
        member=request.user
    ).select_related('class_schedule__trainer__user').order_by('-class_schedule__start_time')
    
    return render(request, 'classes/my_classes.html', {'bookings': bookings})