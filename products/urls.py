from django.urls import path
from . import views, search_api

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('wishlist/', views.view_wishlist, name='view_wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('newsletter/subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('api/stock/<int:product_id>/', views.check_stock, name='check_stock'),
    path('compare/', views.compare_products, name='compare_products'),
    
    # Search & Filter API
    path('api/search/', search_api.live_search, name='api_search'),
    path('api/filter/', search_api.filter_products, name='api_filter'),
    path('api/filter-options/', search_api.get_filter_options, name='api_filter_options'),

    # News, Contact, About
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('consultation/', views.consultation, name='consultation'),
]
