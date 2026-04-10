from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Cart, CartItem
from products.models import Product

def get_cart(request):
    """Helper để lấy hoặc tạo giỏ hàng"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    return None

@login_required(login_url='login')
@require_http_methods(["POST"])
def add_to_cart(request, product_id):
    """Thêm sản phẩm vào giỏ hàng"""
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart = get_cart(request)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity < 1:
        messages.error(request, 'Số lượng không hợp lệ.')
        return redirect('product_detail', pk=product_id)
    
    if product.stock < quantity:
        messages.error(request, 'Không đủ hàng.')
        return redirect('product_detail', pk=product_id)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        if cart_item.quantity > product.stock:
            messages.error(request, 'Không đủ hàng.')
            return redirect('product_detail', pk=product_id)
        cart_item.save()
    
    messages.success(request, f'Đã thêm {product.name} vào giỏ hàng.')
    return redirect('view_cart')


@login_required(login_url='login')
def view_cart(request):
    """Xem giỏ hàng"""
    cart = get_cart(request)
    if cart:
        items = cart.items.all()
    else:
        items = []
        
    context = {
        'cart': cart,
        'cart_items': items,
    }
    return render(request, 'carts/cart.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def update_cart_item(request, item_id):
    """Cập nhật số lượng sản phẩm trong giỏ"""
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity < 1:
        cart_item.delete()
        messages.success(request, 'Đã xóa sản phẩm khỏi giỏ hàng.')
    else:
        if cart_item.product.stock < quantity:
            messages.error(request, 'Không đủ hàng.')
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cập nhật giỏ hàng thành công.')
    
    return redirect('view_cart')


@login_required(login_url='login')
@require_http_methods(["POST"])
def remove_from_cart(request, item_id):
    """Xóa sản phẩm khỏi giỏ hàng"""
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'Đã xóa {product_name} khỏi giỏ hàng.')
    return redirect('view_cart')


def clear_cart(request):
    """Xóa toàn bộ giỏ hàng"""
    if request.method == 'POST':
        cart = get_cart(request)
        if cart:
            cart.items.all().delete()
            messages.success(request, 'Giỏ hàng đã được xóa.')
    return redirect('view_cart')
