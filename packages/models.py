# packages/models.py

from django.db import models

class PackageCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Package Categories"

class PackageType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class MembershipPackage(models.Model):
    name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(PackageCategory, on_delete=models.PROTECT, related_name='packages')
    package_type = models.ForeignKey(PackageType, on_delete=models.PROTECT, related_name='packages')
    duration_days = models.PositiveIntegerField(help_text="Duration in days")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField(help_text="List features separated by newline or commas")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name