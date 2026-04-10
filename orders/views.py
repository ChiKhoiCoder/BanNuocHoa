from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.utils.text import slugify
import uuid
from .models import Order, OrderDetail, Coupon
from .forms import CheckoutForm
from carts.models import Cart, CartItem
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.http import JsonResponse


@login_required(login_url='login')
def checkout(request):
    """Trang thanh toán"""
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, 'Giỏ hàng của bạn trống.')
        return redirect('view_cart')
    
    cart_items = cart.items.all()
    
    # Lấy danh sách item IDs từ query parameter
    item_ids = request.GET.get('items', '').split(',')
    if item_ids and item_ids[0]:
        cart_items = cart_items.filter(id__in=item_ids)
    
    if not cart_items.exists():
        messages.error(request, 'Vui lòng chọn ít nhất một sản phẩm để thanh toán.')
        return redirect('view_cart')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user
                order.order_number = f"ORD-{slugify(request.user.username)}-{uuid.uuid4().hex[:8].upper()}"
                
                # Tính tổng giá chỉ cho các sản phẩm được chọn
                cart_total = sum(item.get_total_price() for item in cart_items)
                shipping_cost = 0  # Free shipping for now

                # Áp dụng mã giảm giá (nếu có)
                coupon_code = form.cleaned_data.get('coupon_code') if hasattr(form, 'cleaned_data') else request.POST.get('coupon_code')
                discount_amount = 0
                if coupon_code:
                    coupon = Coupon.objects.filter(code__iexact=coupon_code).first()
                    if coupon and coupon.is_valid(cart_total):
                        # compute discounted final price
                        new_total = coupon.apply_discount(cart_total)
                        discount_amount = float(cart_total) - float(new_total)
                        order.coupon_code = coupon.code
                        coupon.used_count += 1
                        coupon.save()
                    else:
                        messages.warning(request, 'Mã giảm giá không hợp lệ hoặc đã hết hạn.')

                order.total_price = cart_total
                order.shipping_cost = shipping_cost
                order.final_price = cart_total - discount_amount + shipping_cost
                order.save()
                
                # Tạo order details
                for item in cart_items:
                    OrderDetail.objects.create(
                        order=order,
                        product=item.product,
                        product_name=item.product.name,
                        product_price=item.product.get_price(),
                        quantity=item.quantity
                    )
                    # Cập nhật stock
                    item.product.stock -= item.quantity
                    item.product.save()
                
                # Xóa các item đã thanh toán khỏi giỏ hàng
                cart_items.delete()

                # Gửi email xác nhận đơn hàng (console backend in development)
                try:
                    subject = f'Xác nhận đơn hàng {order.order_number}'
                    message = render_to_string('orders/order_confirmation_email.txt', {'order': order, 'user': request.user})
                    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@example.com')
                    send_mail(subject, message, from_email, [order.email], fail_silently=True)
                except Exception:
                    # Fail silently in development; messages already inform user
                    pass

                messages.success(request, f'Đơn hàng {order.order_number} đã được tạo thành công!')
                return redirect('order_confirmation', order_number=order.order_number)
    else:
        initial_data = {
            'full_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        }
        if hasattr(request.user, 'profile'):
            profile = request.user.profile
            initial_data.update({
                'phone': profile.phone or '',
                'address': profile.address or '',
                'city': profile.city or '',
                'state': profile.state or '',
                'zip_code': profile.zip_code or '',
            })
        form = CheckoutForm(initial=initial_data)
    
    # Tính tổng giá cho các sản phẩm được chọn để hiển thị
    total_price = sum(item.get_total_price() for item in cart_items)
    
    context = {
        'form': form,
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'orders/checkout.html', context)


@login_required(login_url='login')
def order_confirmation(request, order_number):
    """Xác nhận đơn hàng"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    context = {'order': order}
    return render(request, 'orders/order_confirmation.html', context)


@login_required(login_url='login')
def order_list(request):
    """Danh sách đơn hàng"""
    orders = Order.objects.filter(user=request.user)
    
    # Lọc đơn hàng chưa thanh toán nếu có rarameter
    unpaid_only = request.GET.get('unpaid') == '1'
    if unpaid_only:
        orders = orders.filter(is_paid=False)
        
    orders = orders.order_by('-created_at')
    context = {
        'orders': orders,
        'unpaid_only': unpaid_only,
    }
    return render(request, 'orders/order_list.html', context)


@login_required(login_url='login')
def order_detail(request, order_number):
    """Chi tiết đơn hàng"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    order_details = order.details.all()
    context = {
        'order': order,
        'order_details': order_details,
    }
    return render(request, 'orders/order_detail.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def cancel_order(request, order_number):
    """Hủy đơn hàng"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    if order.status in ['pending', 'approved']:
        # Hoàn lại stock
        for detail in order.details.all():
            if detail.product:
                detail.product.stock += detail.quantity
                detail.product.save()
        
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'Đơn hàng đã bị hủy.')
    else:
        messages.error(request, 'Không thể hủy đơn hàng ở trạng thái này.')
    
    return redirect('order_list')


@login_required(login_url='login')
def get_order_status(request, order_number):
    """API endpoint trả về trạng thái đơn hàng để client poll/realtime"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    data = {
        'order_number': order.order_number,
        'status': order.status,
        'is_paid': order.is_paid,
        'updated_at': order.updated_at.isoformat(),
    }
    return JsonResponse(data)


@login_required(login_url='login')
def validate_coupon(request):
    """Validate coupon for current user's cart and return discount/new total as JSON"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)

    coupon_code = request.POST.get('coupon_code', '').strip()
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return JsonResponse({'error': 'Cart not found'}, status=400)

    cart_total = cart.get_total_price()
    if not coupon_code:
        return JsonResponse({'valid': False, 'message': 'Vui lòng cung cấp mã giảm giá.'})

    coupon = Coupon.objects.filter(code__iexact=coupon_code).first()
    if not coupon:
        return JsonResponse({'valid': False, 'message': 'Mã giảm giá không tồn tại.'})

    if not coupon.is_valid(cart_total):
        return JsonResponse({'valid': False, 'message': 'Mã giảm giá không hợp lệ hoặc đã hết hạn.'})

    # compute discount
    new_total = coupon.apply_discount(cart_total)
    discount_amount = float(cart_total) - float(new_total)
    return JsonResponse({
        'valid': True,
        'message': 'Mã giảm giá hợp lệ.',
        'discount': int(discount_amount),
        'new_total': int(new_total),
        'coupon_code': coupon.code,
    })
