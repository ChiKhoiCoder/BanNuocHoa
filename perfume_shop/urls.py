from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('products.urls')),
    path('admin/', admin.site.urls),
    path('admin-panel/', include('products.admin_urls')),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('reviews/', include('reviews.urls')),
    path('payments/', include('payments.urls')),
    path('carts/', include('carts.urls')),
    # django-allauth endpoints (expects django-allauth in settings)
    path('accounts/', include('allauth.urls')),
    path('api/', include('api.urls')),
]

# serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
