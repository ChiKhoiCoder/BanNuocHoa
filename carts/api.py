from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from products.models import Product


def get_cart(request):
    """Helper để lấy hoặc tạo giỏ hàng"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    return None


@login_required
@require_http_methods(["GET"])
def get_cart_data(request):
    """API endpoint để lấy dữ liệu giỏ hàng cho mini cart"""
    cart = get_cart(request)
    
    if not cart:
        return JsonResponse({
            'success': False,
            'message': 'Vui lòng đăng nhập'
        })
    
    items = []
    total = 0
    
    for item in cart.items.all():
        item_total = item.get_total_price()
        items.append({
            'id': item.id,
            'product_id': item.product.id,
            'product_name': item.product.name,
            'product_image': item.product.image.url if item.product.image else '',
            'price': float(item.product.get_price()),
            'quantity': item.quantity,
            'total': float(item_total),
            'stock': item.product.stock,
        })
        total += item_total
    
    return JsonResponse({
        'success': True,
        'items': items,
        'total': float(total),
        'count': cart.items.count(),
    })


@login_required
@require_http_methods(["POST"])
def ajax_add_to_cart(request, product_id):
    """AJAX endpoint để thêm sản phẩm vào giỏ"""
    try:
        product = get_object_or_404(Product, pk=product_id, is_active=True)
        cart = get_cart(request)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity < 1:
            return JsonResponse({
                'success': False,
                'message': 'Số lượng không hợp lệ.'
            })
        
        if product.stock < quantity:
            return JsonResponse({
                'success': False,
                'message': 'Không đủ hàng trong kho.'
            })
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.stock:
                return JsonResponse({
                    'success': False,
                    'message': 'Không đủ hàng trong kho.'
                })
            cart_item.quantity = new_quantity
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Đã thêm {product.name} vào giỏ hàng.',
            'cart_count': cart.items.count(),
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })


@login_required
@require_http_methods(["POST"])
def ajax_update_cart_item(request, item_id):
    """AJAX endpoint để cập nhật số lượng"""
    try:
        cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity < 1:
            cart_item.delete()
            cart = get_cart(request)
            return JsonResponse({
                'success': True,
                'message': 'Đã xóa sản phẩm khỏi giỏ hàng.',
                'cart_count': cart.items.count() if cart else 0,
                'deleted': True,
            })
        
        if cart_item.product.stock < quantity:
            return JsonResponse({
                'success': False,
                'message': 'Không đủ hàng trong kho.'
            })
        
        cart_item.quantity = quantity
        cart_item.save()
        
        cart = get_cart(request)
        cart_total = sum(item.get_total_price() for item in cart.items.all())
        
        return JsonResponse({
            'success': True,
            'message': 'Cập nhật giỏ hàng thành công.',
            'item_total': float(cart_item.get_total_price()),
            'cart_total': float(cart_total),
            'cart_count': cart.items.count(),
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })


@login_required
@require_http_methods(["POST"])
def ajax_remove_from_cart(request, item_id):
    """AJAX endpoint để xóa sản phẩm"""
    try:
        cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
        product_name = cart_item.product.name
        cart_item.delete()
        
        cart = get_cart(request)
        cart_total = sum(item.get_total_price() for item in cart.items.all()) if cart else 0
        
        return JsonResponse({
            'success': True,
            'message': f'Đã xóa {product_name} khỏi giỏ hàng.',
            'cart_total': float(cart_total),
            'cart_count': cart.items.count() if cart else 0,
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })


@login_required
@require_http_methods(["POST"])
def ajax_clear_cart(request):
    """AJAX endpoint để xóa toàn bộ giỏ hàng"""
    try:
        cart = get_cart(request)
        if cart:
            cart.items.all().delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Giỏ hàng đã được xóa.',
            'cart_count': 0,
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })
