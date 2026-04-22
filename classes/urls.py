from django.urls import path
from . import views

app_name = 'classes'

urlpatterns = [
    path('schedule/', views.class_schedule, name='schedule'),
    path('book/<int:class_id>/', views.book_class, name='book'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel'),
    path('my-classes/', views.my_classes, name='my_classes'),
]