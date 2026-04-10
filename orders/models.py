from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    """Đơn hàng"""
    STATUS_CHOICES = (
        ('pending', 'Chờ xác nhận'),
        ('approved', 'Đã xác nhận'),
        ('shipped', 'Đang giao hàng'),
        ('completed', 'Hoàn thành'),
        ('cancelled', 'Hủy bỏ'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10)
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    coupon_code = models.CharField(max_length=50, blank=True, null=True)
    
    payment_method = models.CharField(max_length=50, choices=[
        ('cash', 'Thanh toán khi nhận hàng'),
        ('bank', 'Chuyển khoản ngân hàng'),
        ('credit_card', 'Thẻ tín dụng'),
    ])
    is_paid = models.BooleanField(default=False)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status', '-created_at']),
        ]

    def __str__(self):
        return f"Order {self.order_number}"

    def get_status_display_vn(self):
        """Trả về tên trạng thái bằng tiếng Việt"""
        return dict(self.STATUS_CHOICES).get(self.status, self.status)


class OrderDetail(models.Model):
    """Chi tiết đơn hàng"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    class Meta:
        verbose_name = 'Order Detail'
        verbose_name_plural = 'Order Details'

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"

    def get_total_price(self):
        """Tính tổng giá của item"""
        return self.product_price * self.quantity


class Coupon(models.Model):
    """Mã giảm giá / voucher"""
    CODE_TYPE = (
        ('percent', 'Percent'),
        ('amount', 'Fixed Amount'),
    )
    code = models.CharField(max_length=50, unique=True)
    coupon_type = models.CharField(max_length=10, choices=CODE_TYPE, default='percent')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    usage_limit = models.IntegerField(null=True, blank=True)
    used_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'

    def __str__(self):
        return self.code

    def is_valid(self, amount):
        from django.utils import timezone
        now = timezone.now()
        if not self.is_active:
            return False
        if not (self.start_date <= now <= self.end_date):
            return False
        if self.usage_limit is not None and self.used_count >= self.usage_limit:
            return False
        if amount < self.min_order_amount:
            return False
        return True

    def apply_discount(self, amount):
        if self.coupon_type == 'percent':
            discount = (amount * self.value) / 100
        else:
            discount = self.value
        return max(0, amount - discount)
