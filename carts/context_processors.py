from .utils import get_cart

def cart_context(request):
    """Context processor để hiển thị số lượng giỏ hàng trên navbar"""
    cart = get_cart(request)
    cart_items_count = 0
    if cart:
        cart_items_count = cart.get_total_items()
    return {
        'cart_items_count': cart_items_count,
        'cart': cart,
    }
