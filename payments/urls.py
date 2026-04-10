from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('start/<int:order_id>/<str:provider>/', views.start_payment, name='start'),
    path('simulate/', views.simulate_gateway, name='simulate_gateway'),
    path('return/', views.payment_return, name='payment_return'),
]
