from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from products.models import Product

class Cart(models.Model):
    """Giỏ hàng"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        return f"{self.user.username}'s Cart"

    def get_total_price(self):
        """Tính tổng giá giỏ hàng"""
        return sum(item.get_total_price() for item in self.items.all())

    def get_total_items(self):
        """Tính tổng số sản phẩm"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Các sản phẩm trong giỏ hàng"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_total_price(self):
        """Tính tổng giá của item"""
        return self.product.get_price() * self.quantity
