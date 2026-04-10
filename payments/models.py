from django.db import models
from orders.models import Order


class Transaction(models.Model):
    PROVIDER_CHOICES = (
        ('vnpay', 'VNPay'),
        ('momo', 'Momo'),
        ('sandbox', 'Sandbox'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transactions')
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default='sandbox')
    transaction_id = models.CharField(max_length=200, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return f"{self.provider} - {self.order.order_number} - {self.status}"
