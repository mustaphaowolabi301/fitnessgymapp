# bookings/admin.py

from django.contrib import admin
from django.utils import timezone
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'member', 'package', 'start_date', 'end_date', 'total_amount', 'paid_amount', 'balance_due', 'status')
    list_filter = ('status', 'start_date', 'package__category')
    search_fields = ('member__email', 'member__first_name', 'member__last_name')
    readonly_fields = ('created_at', 'updated_at', 'balance_due')
    actions = ['mark_as_confirmed', 'mark_as_active', 'mark_as_cancelled']
    
    def balance_due(self, obj):
        return obj.balance_due()
    balance_due.short_description = 'Balance Due'
    
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_as_confirmed.short_description = "Mark selected bookings as Confirmed"
    
    def mark_as_active(self, request, queryset):
        queryset.update(status='active')
    mark_as_active.short_description = "Mark selected bookings as Active"
    
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    mark_as_cancelled.short_description = "Mark selected bookings as Cancelled"

admin.site.register(Booking, BookingAdmin)