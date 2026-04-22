# packages/admin.py

from django.contrib import admin
from .models import PackageCategory, PackageType, MembershipPackage

@admin.register(PackageCategory)
class PackageCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(PackageType)
class PackageTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(MembershipPackage)
class MembershipPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'package_type', 'duration_days', 'price', 'is_active')
    list_filter = ('category', 'package_type', 'is_active')
    search_fields = ('name', 'description')