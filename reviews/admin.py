from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['product__name', 'user__username', 'title', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Thông tin đánh giá', {
            'fields': ('product', 'user', 'rating', 'is_approved')
        }),
        ('Nội dung', {
            'fields': ('title', 'comment')
        }),
        ('Các dấu thời gian', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
