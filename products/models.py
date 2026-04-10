from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Category(models.Model):
    """Danh mục sản phẩm"""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """Sản phẩm nước hoa"""
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='products/')
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    brand = models.CharField(max_length=100)
    scent_type = models.CharField(max_length=100, blank=True)  # EDP, EDT, Cologne, etc.
    volume = models.CharField(max_length=50)  # 50ml, 100ml, etc.
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    num_reviews = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', '-created_at']),
            models.Index(fields=['is_active', '-created_at']),
        ]

    def __str__(self):
        return self.name

    def get_price(self):
        """Trả về giá sau giảm giá nếu có"""
        # Check active flash sale for this product
        from django.utils import timezone
        now = timezone.now()
        active_sale = getattr(self, 'flashsales', None)
        if active_sale is not None:
            sale = self.flashsales.filter(is_active=True, start_time__lte=now, end_time__gte=now).first()
            if sale and sale.discount_price:
                return sale.discount_price
        if self.discount_price:
            return self.discount_price
        return self.price

    def get_discount_percent(self):
        """Tính phần trăm giảm giá (bao gồm cả Flash Sale)"""
        current_price = self.get_price()
        if current_price < self.price and self.price > 0:
            return int(((self.price - current_price) / self.price) * 100)
        return 0


class FlashSale(models.Model):
    """Flash sale áp dụng cho sản phẩm trong khoảng thời gian"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='flashsales')
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Flash Sale'
        verbose_name_plural = 'Flash Sales'

    def __str__(self):
        return f"FlashSale {self.product.name} ({self.start_time.date()} - {self.end_time.date()})"

    def get_discount_percent(self):
        """Tính phần trăm giảm giá"""
        if self.discount_price and self.product.price > 0:
            return int(((self.product.price - self.discount_price) / self.product.price) * 100)
        return 0


class WishlistItem(models.Model):
    """Sản phẩm yêu thích của người dùng"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Wishlist Item'
        verbose_name_plural = 'Wishlist Items'
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} -> {self.product.name}"


class NewsletterSubscriber(models.Model):
    """Subscriber for marketing newsletter"""
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Newsletter Subscriber'
        verbose_name_plural = 'Newsletter Subscribers'

    def __str__(self):
        return self.email
class NewsPost(models.Model):
    """Bài viết tin tức"""
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'News Post'
        verbose_name_plural = 'News Posts'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    """Tin nhắn liên hệ từ người dùng"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
