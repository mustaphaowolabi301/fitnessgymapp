# core/urls.py

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('trainers/', views.trainers_list, name='trainers'),
    path('equipment/', views.equipment, name='equipment'),
    path('plans/', views.membership_plans, name='plans'),
    path('contact/', views.contact, name='contact'),
]