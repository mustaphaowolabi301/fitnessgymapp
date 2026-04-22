# bookings/urls.py

from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('apply/<int:package_id>/', views.apply_package, name='apply'),
    path('history/', views.booking_history, name='history'),
    path('detail/<int:booking_id>/', views.booking_detail, name='detail'),
    path('payment/<int:booking_id>/', views.make_payment, name='make_payment'),  # For online payment (optional)
]