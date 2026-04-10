from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone', 'city', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'phone', 'email']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Thông tin người dùng', {
            'fields': ('user', 'role')
        }),
        ('Thông tin liên hệ', {
            'fields': ('phone', 'address', 'city', 'state', 'zip_code')
        }),
        ('Thông tin cá nhân', {
            'fields': ('date_of_birth', 'avatar')
        }),
        ('Các dấu thời gian', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
