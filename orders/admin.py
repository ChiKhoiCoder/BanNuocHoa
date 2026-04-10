from django.contrib import admin
from .models import Order, OrderDetail
from .models import Coupon


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    readonly_fields = ['product_name', 'product_price', 'quantity']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'final_price', 'status', 'is_paid', 'created_at']
    list_filter = ['status', 'is_paid', 'created_at', 'payment_method']
    search_fields = ['order_number', 'user__username', 'email', 'phone']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderDetailInline]
    fieldsets = (
        ('Thông tin đơn hàng', {
            'fields': ('order_number', 'user', 'status', 'created_at', 'updated_at')
        }),
        ('Thông tin giao hàng', {
            'fields': ('full_name', 'email', 'phone', 'address', 'city', 'state', 'zip_code')
        }),
        ('Thông tin thanh toán', {
            'fields': ('total_price', 'shipping_cost', 'final_price', 'payment_method', 'is_paid')
        }),
        ('Ghi chú', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'order', 'quantity', 'product_price']
    list_filter = ['order__created_at']
    search_fields = ['product_name', 'order__order_number']
    readonly_fields = ['product_name', 'product_price']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'coupon_type', 'value', 'start_date', 'end_date', 'is_active', 'used_count']
    list_filter = ['coupon_type', 'is_active', 'start_date', 'end_date']
    search_fields = ['code']
