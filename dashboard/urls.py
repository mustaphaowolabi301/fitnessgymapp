# dashboard/urls.py

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.admin_dashboard, name='index'),
    
    # Categories CRUD
    path('categories/', views.category_list, name='categories'),
    path('categories/add/', views.category_create, name='category_add'),
    path('categories/<int:pk>/edit/', views.category_update, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    # Package Types CRUD
    path('package-types/', views.package_type_list, name='package_types'),
    path('package-types/add/', views.package_type_create, name='package_type_add'),
    path('package-types/<int:pk>/edit/', views.package_type_update, name='package_type_edit'),
    path('package-types/<int:pk>/delete/', views.package_type_delete, name='package_type_delete'),
    
    # Packages CRUD
    path('packages/', views.package_list, name='packages'),
    path('packages/add/', views.package_create, name='package_add'),
    path('packages/<int:pk>/edit/', views.package_update, name='package_edit'),
    path('packages/<int:pk>/delete/', views.package_delete, name='package_delete'),
    
    # Other management (to be implemented)
    path('bookings/', views.manage_bookings, name='bookings'),
    path('payments/', views.manage_payments, name='payments'),
    path('reports/', views.reports, name='reports'),
    path('reports/results/', views.reports_results, name='reports_results'),

    path('bookings/', views.manage_bookings, name='bookings'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
    
    path('trainers/', views.trainer_list, name='trainers'),
    path('trainers/add/', views.trainer_create, name='trainer_add'),
    path('trainers/<int:pk>/edit/', views.trainer_update, name='trainer_edit'),
    path('trainers/<int:pk>/delete/', views.trainer_delete, name='trainer_delete'),
    
    path('classes/', views.class_list, name='classes'),
    path('classes/add/', views.class_create, name='class_add'),
    path('classes/<int:pk>/edit/', views.class_update, name='class_edit'),
    path('classes/<int:pk>/delete/', views.class_delete, name='class_delete'),
    path('class-bookings/', views.class_booking_list, name='class_bookings'),
    path('reports/', views.reports, name='reports'),
    path('pos/', views.pos, name='pos'),
    
    path('email/compose/', views.email_campaign, name='email_compose'),
path('email/history/', views.email_campaign_history, name='email_campaign_history'),
]
