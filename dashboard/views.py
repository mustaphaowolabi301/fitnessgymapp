from django.utils import timezone
from bookings.models import Booking
from payments.models import Payment
from accounts.models import User
from .forms import PaymentForm, BookingStatusForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from bookings.models import Booking
from payments.models import Payment
from accounts.models import User
from packages.models import PackageCategory, PackageType, MembershipPackage
from .forms import PackageCategoryForm, PackageTypeForm, MembershipPackageForm
from datetime import datetime, timedelta
from trainers.models import Trainer
from .forms import TrainerForm
from classes.models import ClassSchedule
from .forms import ClassScheduleForm
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse   # <-- Add this line
from django.http import HttpResponse
from django.db.models import Count, Sum, Q
from datetime import datetime
from bookings.models import Booking
from accounts.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db import transaction
from datetime import timedelta
from accounts.models import User
from packages.models import MembershipPackage
from bookings.models import Booking
from payments.models import Payment
from .forms import POSLookupForm, POSPackageSelectForm, POSPaymentForm
from communication.models import EmailCampaign
from django.core.mail import send_mass_mail
from .forms import EmailCampaignForm

# ---------- Dashboard Home ----------
@staff_member_required
def admin_dashboard(request):
    total_members = User.objects.filter(is_staff=False).count()
    active_bookings = Booking.objects.filter(status='active').count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    total_revenue = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0
    recent_bookings = Booking.objects.order_by('-created_at')[:10]
    
    context = {
        'total_members': total_members,
        'active_bookings': active_bookings,
        'pending_bookings': pending_bookings,
        'total_revenue': total_revenue,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'dashboard/index.html', context)


# ---------- Category CRUD (using function-based views for simplicity) ----------
@staff_member_required
def category_list(request):
    categories = PackageCategory.objects.all().order_by('name')
    return render(request, 'dashboard/category_list.html', {'categories': categories})

@staff_member_required
def category_create(request):
    if request.method == 'POST':
        form = PackageCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully.')
            return redirect('dashboard:categories')
    else:
        form = PackageCategoryForm()
    return render(request, 'dashboard/category_form.html', {'form': form, 'title': 'Add Category'})

@staff_member_required
def category_update(request, pk):
    category = get_object_or_404(PackageCategory, pk=pk)
    if request.method == 'POST':
        form = PackageCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('dashboard:categories')
    else:
        form = PackageCategoryForm(instance=category)
    return render(request, 'dashboard/category_form.html', {'form': form, 'title': 'Edit Category'})

@staff_member_required
def category_delete(request, pk):
    category = get_object_or_404(PackageCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('dashboard:categories')
    return render(request, 'dashboard/confirm_delete.html', {'object': category, 'cancel_url': 'dashboard:categories'})


# ---------- Package Type CRUD ----------
@staff_member_required
def package_type_list(request):
    types = PackageType.objects.all().order_by('name')
    return render(request, 'dashboard/package_type_list.html', {'types': types})

@staff_member_required
def package_type_create(request):
    if request.method == 'POST':
        form = PackageTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Package type created successfully.')
            return redirect('dashboard:package_types')
    else:
        form = PackageTypeForm()
    return render(request, 'dashboard/package_type_form.html', {'form': form, 'title': 'Add Package Type'})

@staff_member_required
def package_type_update(request, pk):
    ptype = get_object_or_404(PackageType, pk=pk)
    if request.method == 'POST':
        form = PackageTypeForm(request.POST, instance=ptype)
        if form.is_valid():
            form.save()
            messages.success(request, 'Package type updated successfully.')
            return redirect('dashboard:package_types')
    else:
        form = PackageTypeForm(instance=ptype)
    return render(request, 'dashboard/package_type_form.html', {'form': form, 'title': 'Edit Package Type'})

@staff_member_required
def package_type_delete(request, pk):
    ptype = get_object_or_404(PackageType, pk=pk)
    if request.method == 'POST':
        ptype.delete()
        messages.success(request, 'Package type deleted successfully.')
        return redirect('dashboard:package_types')
    return render(request, 'dashboard/confirm_delete.html', {'object': ptype, 'cancel_url': 'dashboard:package_types'})


# ---------- Membership Package CRUD ----------
@staff_member_required
def package_list(request):
    packages = MembershipPackage.objects.select_related('category', 'package_type').all().order_by('name')
    return render(request, 'dashboard/package_list.html', {'packages': packages})

@staff_member_required
def package_create(request):
    if request.method == 'POST':
        form = MembershipPackageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Package created successfully.')
            return redirect('dashboard:packages')
    else:
        form = MembershipPackageForm()
    return render(request, 'dashboard/package_form.html', {'form': form, 'title': 'Add Package'})

@staff_member_required
def package_update(request, pk):
    package = get_object_or_404(MembershipPackage, pk=pk)
    if request.method == 'POST':
        form = MembershipPackageForm(request.POST, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, 'Package updated successfully.')
            return redirect('dashboard:packages')
    else:
        form = MembershipPackageForm(instance=package)
    return render(request, 'dashboard/package_form.html', {'form': form, 'title': 'Edit Package'})

@staff_member_required
def package_delete(request, pk):
    package = get_object_or_404(MembershipPackage, pk=pk)
    if request.method == 'POST':
        package.delete()
        messages.success(request, 'Package deleted successfully.')
        return redirect('dashboard:packages')
    return render(request, 'dashboard/confirm_delete.html', {'object': package, 'cancel_url': 'dashboard:packages'})


# ---------- Placeholders for other management ----------
@staff_member_required
def manage_bookings(request):
    bookings = Booking.objects.select_related('member', 'package').all().order_by('-created_at')
    return render(request, 'dashboard/booking_list.html', {'bookings': bookings})

@staff_member_required
def manage_payments(request):
    payments = Payment.objects.select_related('booking__member', 'received_by').all().order_by('-payment_date')
    return render(request, 'dashboard/payment_list.html', {'payments': payments})

@staff_member_required
def reports(request):
    return render(request, 'dashboard/reports.html')

# ---------- Booking Management ----------
@staff_member_required
def manage_bookings(request):
    bookings = Booking.objects.select_related('member', 'package').all().order_by('-created_at')
    
    # Filtering
    status = request.GET.get('status')
    member_email = request.GET.get('member_email')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if status:
        bookings = bookings.filter(status=status)
    if member_email:
        bookings = bookings.filter(member__email__icontains=member_email)
    if date_from:
        bookings = bookings.filter(start_date__gte=date_from)
    if date_to:
        bookings = bookings.filter(start_date__lte=date_to)
    
    return render(request, 'dashboard/booking_list.html', {
        'bookings': bookings,
        'status_choices': Booking.STATUS_CHOICES,
        'current_filters': {
            'status': status,
            'member_email': member_email,
            'date_from': date_from,
            'date_to': date_to,
        }
    })

@staff_member_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    payments = booking.payments.all().order_by('-payment_date')
    
    if request.method == 'POST':
        if 'add_payment' in request.POST:
            payment_form = PaymentForm(request.POST)
            status_form = BookingStatusForm(instance=booking)
            if payment_form.is_valid():
                payment = payment_form.save(commit=False)
                payment.booking = booking
                payment.received_by = request.user
                payment.save()
                messages.success(request, f'Payment of ${payment.amount} recorded.')
                return redirect('dashboard:booking_detail', pk=pk)
        elif 'update_status' in request.POST:
            status_form = BookingStatusForm(request.POST, instance=booking)
            payment_form = PaymentForm()
            if status_form.is_valid():
                status_form.save()
                messages.success(request, f'Booking status updated to {booking.get_status_display()}.')
                return redirect('dashboard:booking_detail', pk=pk)
    else:
        payment_form = PaymentForm()
        status_form = BookingStatusForm(instance=booking)
    
    return render(request, 'dashboard/booking_detail.html', {
        'booking': booking,
        'payments': payments,
        'payment_form': payment_form,
        'status_form': status_form,
    })
    
@staff_member_required
def trainer_list(request):
    trainers = Trainer.objects.select_related('user').all().order_by('user__first_name')
    return render(request, 'dashboard/trainer_list.html', {'trainers': trainers})

@staff_member_required
def trainer_create(request):
    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Trainer created successfully.')
            return redirect('dashboard:trainers')
    else:
        form = TrainerForm()
    return render(request, 'dashboard/trainer_form.html', {'form': form, 'title': 'Add Trainer'})

@staff_member_required
def trainer_update(request, pk):
    trainer = get_object_or_404(Trainer, pk=pk)
    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES, instance=trainer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Trainer updated successfully.')
            return redirect('dashboard:trainers')
    else:
        form = TrainerForm(instance=trainer)
    return render(request, 'dashboard/trainer_form.html', {'form': form, 'title': 'Edit Trainer'})

@staff_member_required
def trainer_delete(request, pk):
    trainer = get_object_or_404(Trainer, pk=pk)
    if request.method == 'POST':
        trainer.delete()
        messages.success(request, 'Trainer deleted successfully.')
        return redirect('dashboard:trainers')
    return render(request, 'dashboard/confirm_delete.html', {'object': trainer, 'cancel_url': 'dashboard:trainers'})

@staff_member_required
def class_list(request):
    classes = ClassSchedule.objects.select_related('trainer__user').all().order_by('start_time')
    return render(request, 'dashboard/class_list.html', {'classes': classes})

@staff_member_required
def class_create(request):
    if request.method == 'POST':
        form = ClassScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class created successfully.')
            return redirect('dashboard:classes')
    else:
        form = ClassScheduleForm()
    return render(request, 'dashboard/class_form.html', {'form': form, 'title': 'Add Class'})

@staff_member_required
def class_update(request, pk):
    class_obj = get_object_or_404(ClassSchedule, pk=pk)
    if request.method == 'POST':
        form = ClassScheduleForm(request.POST, instance=class_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class updated successfully.')
            return redirect('dashboard:classes')
    else:
        form = ClassScheduleForm(instance=class_obj)
    return render(request, 'dashboard/class_form.html', {'form': form, 'title': 'Edit Class'})

@staff_member_required
def class_delete(request, pk):
    class_obj = get_object_or_404(ClassSchedule, pk=pk)
    if request.method == 'POST':
        class_obj.delete()
        messages.success(request, 'Class deleted successfully.')
        return redirect('dashboard:classes')
    return render(request, 'dashboard/confirm_delete.html', {'object': class_obj, 'cancel_url': 'dashboard:classes'})

@staff_member_required
def class_booking_list(request):
    bookings = ClassBooking.objects.select_related('member', 'class_schedule').all().order_by('-class_schedule__start_time')
    return render(request, 'dashboard/class_booking_list.html', {'bookings': bookings})
@staff_member_required
@staff_member_required
@staff_member_required
def reports_form(request):
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    return render(request, 'dashboard/reports.html', {
        'start_date': start_date,
        'end_date': end_date,
    })

@staff_member_required
def reports_results(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    report_type = request.GET.get('report_type', 'bookings')
    
    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)
    
    if report_type == 'bookings':
        data = Booking.objects.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        ).select_related('member', 'package')
        template = 'dashboard/reports/bookings_report.html'
        
        total_bookings = data.count()
        agg = data.aggregate(
            total_revenue=Sum('total_amount'),
            total_paid=Sum('paid_amount')
        )
        context = {
            'data': data,
            'start_date': start_date,
            'end_date': end_date,
            'total_bookings': total_bookings,
            'total_revenue': agg['total_revenue'] or 0,
            'total_paid': agg['total_paid'] or 0,
            'total_pending': (agg['total_revenue'] or 0) - (agg['total_paid'] or 0),
        }
    else:
        data = User.objects.filter(
            date_joined__date__gte=start_date,
            date_joined__date__lte=end_date,
            is_staff=False
        )
        template = 'dashboard/reports/users_report.html'
        context = {
            'data': data,
            'start_date': start_date,
            'end_date': end_date,
        }
    
    if request.GET.get('export') == 'csv':
        return export_csv(data, report_type, start_date, end_date)
    
    return render(request, template, context)

def export_csv(data, report_type, start_date, end_date):
    response = HttpResponse(content_type='text/csv')
    filename = f"{report_type}_report_{start_date}_to_{end_date}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    writer = csv.writer(response)
    
    if report_type == 'bookings':
        writer.writerow(['Booking ID', 'Member', 'Email', 'Package', 'Start Date', 'End Date', 'Total', 'Paid', 'Status', 'Created'])
        for booking in data:
            writer.writerow([
                booking.id,
                booking.member.get_full_name(),
                booking.member.email,
                booking.package.name,
                booking.start_date,
                booking.end_date,
                booking.total_amount,
                booking.paid_amount,
                booking.get_status_display(),
                booking.created_at.date(),
            ])
    else:
        writer.writerow(['User ID', 'Full Name', 'Email', 'Phone', 'Date Joined'])
        for user in data:
            writer.writerow([
                user.id,
                user.get_full_name(),
                user.email,
                user.phone,
                user.date_joined.date(),
            ])
    
    return response
@staff_member_required
def reports(request):
    # Default date range: last 30 days
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    if request.method == 'POST' or request.GET.get('generate'):
        start_date_str = request.GET.get('start_date') or request.POST.get('start_date')
        end_date_str = request.GET.get('end_date') or request.POST.get('end_date')
        report_type = request.GET.get('report_type', 'bookings')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        if report_type == 'bookings':
            data = Booking.objects.filter(
                created_at__date__gte=start_date,
                created_at__date__lte=end_date
            ).select_related('member', 'package')
            template = 'dashboard/reports/bookings_report.html'
            
            # Calculate aggregates
            total_bookings = data.count()
            agg = data.aggregate(
                total_revenue=Sum('total_amount'),
                total_paid=Sum('paid_amount')
            )
            total_revenue = agg['total_revenue'] or 0
            total_paid = agg['total_paid'] or 0
            total_pending = total_revenue - total_paid
            
        else:  # registered users
            data = User.objects.filter(
                date_joined__date__gte=start_date,
                date_joined__date__lte=end_date,
                is_staff=False
            )
            template = 'dashboard/reports/users_report.html'
            total_bookings = None  # not applicable
            total_revenue = total_paid = total_pending = None
        
        # Handle export
        if request.GET.get('export') == 'csv':
            return export_csv(data, report_type, start_date, end_date)
        
        context = {
            'data': data,
            'start_date': start_date,
            'end_date': end_date,
            'report_type': report_type,
        }
        if report_type == 'bookings':
            context.update({
                'total_bookings': total_bookings,
                'total_revenue': total_revenue,
                'total_paid': total_paid,
                'total_pending': total_pending,
            })
        return render(request, template, context)
    
    return render(request, 'dashboard/reports.html', {
        'start_date': start_date,
        'end_date': end_date,
    })

@staff_member_required
def pos(request):
    # Step handling: member_lookup -> select_package -> payment -> confirm
    step = request.GET.get('step', 'lookup')
    member_id = request.session.get('pos_member_id')
    
    if step == 'lookup' or not member_id:
        if request.method == 'POST':
            form = POSLookupForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                try:
                    if email:
                        member = User.objects.get(email=email, is_staff=False)
                    else:
                        member = User.objects.get(phone=phone, is_staff=False)
                    request.session['pos_member_id'] = member.id
                    return redirect(f"{reverse('dashboard:pos')}?step=select_package")
                except User.DoesNotExist:
                    messages.error(request, "Member not found. Please register first.")
        else:
            form = POSLookupForm()
        return render(request, 'dashboard/pos/lookup.html', {'form': form})
    
    member = get_object_or_404(User, id=member_id, is_staff=False)
    
    if step == 'select_package':
        packages = MembershipPackage.objects.filter(is_active=True)
        if request.method == 'POST':
            form = POSPackageSelectForm(request.POST, packages=packages)
            if form.is_valid():
                package_id = form.cleaned_data['package']
                request.session['pos_package_id'] = package_id
                return redirect(f"{reverse('dashboard:pos')}?step=payment")
        else:
            form = POSPackageSelectForm(packages=packages)
        return render(request, 'dashboard/pos/select_package.html', {
            'form': form,
            'member': member,
            'packages': packages,
        })
    
    if step == 'payment':
        package_id = request.session.get('pos_package_id')
        if not package_id:
            messages.error(request, "Please select a package first.")
            return redirect(f"{reverse('dashboard:pos')}?step=select_package")
        package = get_object_or_404(MembershipPackage, id=package_id)
        if request.method == 'POST':
            form = POSPaymentForm(request.POST)
            if form.is_valid():
                # Process transaction
                with transaction.atomic():
                    start_date = form.cleaned_data['start_date']
                    end_date = start_date + timedelta(days=package.duration_days)
                    # Create booking
                    booking = Booking.objects.create(
                        member=member,
                        package=package,
                        start_date=start_date,
                        end_date=end_date,
                        total_amount=package.price,
                        paid_amount=package.price,  # full payment at POS
                        status='confirmed'
                    )
                    # Record payment
                    Payment.objects.create(
                        booking=booking,
                        amount=package.price,
                        payment_mode=form.cleaned_data['payment_mode'],
                        transaction_id=form.cleaned_data.get('transaction_id', ''),
                        received_by=request.user,
                        remarks=form.cleaned_data.get('remarks', 'POS Transaction')
                    )
                    # Clear session
                    del request.session['pos_member_id']
                    del request.session['pos_package_id']
                    request.session['pos_booking_id'] = booking.id
                    return redirect(f"{reverse('dashboard:pos')}?step=receipt")
        else:
            form = POSPaymentForm(initial={'start_date': timezone.now().date()})
        return render(request, 'dashboard/pos/payment.html', {
            'form': form,
            'member': member,
            'package': package,
            'total': package.price,
        })
    
    if step == 'receipt':
        booking_id = request.session.get('pos_booking_id')
        if not booking_id:
            messages.info(request, "No recent transaction.")
            return redirect('dashboard:pos')
        booking = get_object_or_404(Booking, id=booking_id)
        del request.session['pos_booking_id']
        return render(request, 'dashboard/pos/receipt.html', {'booking': booking})
    
    # Fallback
    return redirect('dashboard:pos')

@staff_member_required
def email_campaign(request):
    if request.method == 'POST':
        form = EmailCampaignForm(request.POST)
        if form.is_valid():
            filter_type = form.cleaned_data['recipient_filter']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            
            # Build recipient queryset based on filter
            recipients = User.objects.filter(is_active=True, is_staff=False)
            
            if filter_type == 'all_active':
                # already filtered
                pass
            elif filter_type == 'package':
                package = form.cleaned_data['package']
                # Members with active booking of this package
                recipients = recipients.filter(
                    bookings__package=package,
                    bookings__status='active'
                ).distinct()
            elif filter_type == 'pending_payment':
                recipients = recipients.filter(
                    bookings__paid_amount__lt=models.F('bookings__total_amount'),
                    bookings__status__in=['confirmed', 'active']
                ).distinct()
            elif filter_type == 'expiring_soon':
                thirty_days_later = timezone.now().date() + timedelta(days=30)
                recipients = recipients.filter(
                    bookings__end_date__lte=thirty_days_later,
                    bookings__status='active'
                ).distinct()
            
            recipient_emails = list(recipients.values_list('email', flat=True))
            recipient_count = len(recipient_emails)
            
            if request.POST.get('send') == 'true' and recipient_count > 0:
                # Prepare email datatuple: (subject, message, from_email, [to_email])
                from_email = settings.DEFAULT_FROM_EMAIL
                email_messages = [(subject, body, from_email, [email]) for email in recipient_emails]
                send_mass_mail(email_messages, fail_silently=False)
                
                # Log campaign
                EmailCampaign.objects.create(
                    subject=subject,
                    body=body,
                    recipient_count=recipient_count,
                    sent_by=request.user,
                    filter_criteria=form.cleaned_data
                )
                messages.success(request, f"Email sent to {recipient_count} recipients.")
                return redirect('dashboard:email_campaign_history')
            else:
                # Preview mode
                return render(request, 'dashboard/email/preview.html', {
                    'form': form,
                    'recipient_count': recipient_count,
                    'sample_emails': recipient_emails[:5],
                    'subject': subject,
                    'body': body,
                })
    else:
        form = EmailCampaignForm()
    
    return render(request, 'dashboard/email/compose.html', {'form': form})

@staff_member_required
def email_campaign_history(request):
    campaigns = EmailCampaign.objects.all().order_by('-sent_at')
    return render(request, 'dashboard/email/history.html', {'campaigns': campaigns})
