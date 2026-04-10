from carts.models import Cart


def get_cart(request):
    """Return a Cart for the authenticated user, or None for anonymous users."""
    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart
    return None
