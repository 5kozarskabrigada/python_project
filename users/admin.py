from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'is_banned', 'is_staff']
    list_filter = ['role', 'is_banned', 'is_staff']
    search_fields = ['username', 'email']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Roles & Status', {'fields': ('role', 'is_banned', 'is_active', 'is_staff', 'is_superuser')}),
    )