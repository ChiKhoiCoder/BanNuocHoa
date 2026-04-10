from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.auth, name='auth'),
    path('register/', views.register, name='register'),
    path('register/success/', views.register_success, name='register_success'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
]
