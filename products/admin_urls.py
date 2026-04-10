from django.urls import path
from .admin_views import (
    admin_dashboard, admin_products, admin_orders, admin_users,
    admin_order_detail, admin_user_detail, admin_statistics,
    admin_product_add, admin_product_edit, admin_product_delete
)

urlpatterns = [
    path('', admin_dashboard, name='admin_dashboard'),
    path('dashboard/', admin_dashboard, name='admin_dashboard_alt'),
    path('products/', admin_products, name='admin_products'),
    path('orders/', admin_orders, name='admin_orders'),
    path('orders/<int:order_id>/', admin_order_detail, name='admin_order_detail'),
    path('users/', admin_users, name='admin_users'),
    path('users/<int:user_id>/', admin_user_detail, name='admin_user_detail'),
    path('statistics/', admin_statistics, name='admin_statistics'),
    
    # Product management
    path('products/add/', admin_product_add, name='admin_product_add'),
    path('products/edit/<int:product_id>/', admin_product_edit, name='admin_product_edit'),
    path('products/delete/<int:product_id>/', admin_product_delete, name='admin_product_delete'),
]
