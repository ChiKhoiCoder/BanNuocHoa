from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Transaction
from orders.models import Order


def start_payment(request, order_id, provider):
    """Create a Transaction and redirect to a simulated gateway page."""
    order = get_object_or_404(Order, id=order_id)
    tx = Transaction.objects.create(order=order, provider=provider, amount=order.final_price, status='pending')
    return redirect(reverse('payments:simulate_gateway') + f"?tx_id={tx.id}")


def simulate_gateway(request):
    """A simple page that simulates a gateway UI for testing local flows."""
    tx_id = request.GET.get('tx_id')
    tx = get_object_or_404(Transaction, id=tx_id)
    return render(request, 'payments/simulate_gateway.html', {'tx': tx})


@csrf_exempt
def payment_return(request):
    """Gateway return/webhook handler (simple, supports GET/POST)."""
    tx_id = request.POST.get('tx_id') or request.GET.get('tx_id')
    result = request.POST.get('result') or request.GET.get('result') or 'success'
    tx = get_object_or_404(Transaction, id=tx_id)
    if result == 'success':
        tx.status = 'success'
        tx.transaction_id = f"SIM{tx.id}"
        tx.save()
        order = tx.order
        order.is_paid = True
        order.status = 'approved'
        order.save()
        return render(request, 'payments/payment_return.html', {'success': True, 'order': order})

    tx.status = 'failed'
    tx.save()
    return render(request, 'payments/payment_return.html', {'success': False, 'order': tx.order})
