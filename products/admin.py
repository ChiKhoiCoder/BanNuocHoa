from django.contrib import admin
from .models import Category, Product
from .models import WishlistItem, FlashSale, NewsletterSubscriber


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'discount_price', 'stock', 'is_featured', 'is_active', 'created_at']
    list_filter = ['category', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'brand', 'description']
    readonly_fields = ['rating', 'num_reviews', 'created_at', 'updated_at']
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'category', 'brand', 'scent_type', 'volume')
        }),
        ('Giá cả', {
            'fields': ('price', 'discount_price')
        }),
        ('Mô tả', {
            'fields': ('description', 'image')
        }),
        ('Kho hàng', {
            'fields': ('stock',)
        }),
        ('Đánh giá', {
            'fields': ('rating', 'num_reviews'),
            'classes': ('collapse',)
        }),
        ('Cài đặt', {
            'fields': ('is_featured', 'is_active')
        }),
        ('Các dấu thời gian', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    search_fields = ['user__username', 'product__name']
    readonly_fields = ['created_at']


@admin.register(FlashSale)
class FlashSaleAdmin(admin.ModelAdmin):
    list_display = ['product', 'discount_price', 'start_time', 'end_time', 'is_active']
    list_filter = ['is_active', 'start_time', 'end_time']
    search_fields = ['product__name']


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'created_at']
    search_fields = ['email']
    readonly_fields = ['created_at']
