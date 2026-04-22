# payments/admin.py

from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'amount', 'payment_date', 'payment_mode', 'received_by')
    list_filter = ('payment_mode', 'payment_date')
    search_fields = ('booking__member__email', 'transaction_id')
    readonly_fields = ('payment_date',)
    
    def save_model(self, request, obj, form, change):
        if not obj.received_by:
            obj.received_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Payment, PaymentAdmin)

# Also add inline to Booking admin for convenience
from bookings.admin import BookingAdmin
from bookings.models import Booking

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1
    fields = ('amount', 'payment_mode', 'transaction_id', 'remarks')
    readonly_fields = ('payment_date', 'received_by')
    
    def save_model(self, request, obj, form, change):
        if not obj.received_by:
            obj.received_by = request.user
        super().save_model(request, obj, form, change)

# Unregister and re-register BookingAdmin with inline
admin.site.unregister(Booking)
@admin.register(Booking)
class BookingAdminWithPayments(BookingAdmin):
    inlines = [PaymentInline]