from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'provider', 'amount', 'status', 'created_at')
    list_filter = ('provider', 'status')
    search_fields = ('order__order_number', 'transaction_id')
