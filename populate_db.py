import os
import django
import random
from datetime import timedelta
from django.utils import timezone
from django.core.files.base import ContentFile

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'perfume_shop.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile
from products.models import Category, Product
from orders.models import Order, OrderDetail
from reviews.models import Review

def create_users():
    print("Creating users...")
    # Admin
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        # Profile created by signal, update it
        if hasattr(admin, 'profile'):
            profile = admin.profile
            profile.role = 'admin'
            profile.phone = '0909090909'
            profile.address = 'Admin HQ'
            profile.save()
        print("Admin created: admin/admin123")
    
    # User
    if not User.objects.filter(username='user').exists():
        user = User.objects.create_user('user', 'user@example.com', 'user123')
        if hasattr(user, 'profile'):
            profile = user.profile
            profile.role = 'user'
            profile.phone = '0912345678'
            profile.address = 'User Home'
            profile.save()
        print("User created: user/user123")
    
    # Guest
    if not User.objects.filter(username='guest').exists():
        guest = User.objects.create_user('guest', 'guest@example.com', 'guest123')
        if hasattr(guest, 'profile'):
            guest.profile.role = 'guest'
            guest.profile.save()
        print("Guest created: guest/guest123")

def create_categories():
    print("Creating categories...")
    categories = ['Nam', 'Nữ', 'Unisex', 'Niche', 'Gift Set']
    objs = []
    for name in categories:
        cat, created = Category.objects.get_or_create(name=name, defaults={'description': f'Nước hoa {name} cao cấp'})
        if created:
            objs.append(cat)
    print(f"Created {len(objs)} categories.")
    return Category.objects.all()

def create_products(categories):
    print("Creating products...")
    brands = ['Chanel', 'Dior', 'Gucci', 'Versace', 'Tom Ford', 'Yves Saint Laurent']
    products_data = [
        ('Bleu de Chanel', 'Nam', 3500000),
        ('Chanel No.5', 'Nữ', 4200000),
        ('Dior Sauvage', 'Nam', 3200000),
        ('Miss Dior', 'Nữ', 3800000),
        ('Gucci Bloom', 'Nữ', 2900000),
        ('Versace Eros', 'Nam', 2100000),
        ('Tom Ford Black Orchid', 'Unisex', 4500000),
        ('YSL Libre', 'Nữ', 3600000),
        ('Creed Aventus', 'Niche', 8500000),
        ('Le Labo Santal 33', 'Niche', 6200000),
    ]

    for name, cat_name, price in products_data:
        category = categories.filter(name=cat_name).first()
        if not category:
            category = categories.first()
        
        Product.objects.get_or_create(
            name=name,
            defaults={
                'category': category,
                'description': f'Mô tả chi tiết cho sản phẩm {name}. Hương thơm quyến rũ, lưu hương lâu.',
                'price': price,
                'stock': random.randint(10, 100),
                'brand': random.choice(brands),
                'scent_type': random.choice(['EDP', 'EDT', 'Parfum']),
                'volume': '100ml',
                'is_featured': random.choice([True, False]),
                'is_active': True
            }
        )
    print("Products created.")

def create_orders():
    print("Creating orders...")
    users = User.objects.exclude(is_superuser=True)
    products = Product.objects.all()
    
    if not users.exists() or not products.exists():
        return

    statuses = ['completed', 'pending', 'shipped', 'cancelled']
    
    # Create orders for past 30 days
    for i in range(20):
        user = random.choice(users)
        created_at = timezone.now() - timedelta(days=random.randint(0, 30))
        status = random.choice(statuses)
        
        order = Order.objects.create(
            user=user,
            order_number=f"ORD-DEMO-{random.randint(1000, 9999)}",
            full_name=user.username,
            email=user.email,
            phone='0123456789',
            address='Demo Address',
            city='TP.HCM',
            zip_code='70000',
            total_price=0,
            final_price=0,
            status=status,
            payment_method='cod'
        )
        order.created_at = created_at
        order.save()
        
        # Details
        total = 0
        for _ in range(random.randint(1, 4)):
            product = random.choice(products)
            qty = random.randint(1, 3)
            price = product.price
            OrderDetail.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                product_price=price,
                quantity=qty
            )
            total += price * qty
        
        order.total_price = total
        order.final_price = total
        order.save()
    print("Orders created.")

def create_reviews():
    print("Creating reviews...")
    users = User.objects.exclude(is_superuser=True)
    products = Product.objects.all()
    
    for i in range(15):
        user = random.choice(users)
        product = random.choice(products)
        if not Review.objects.filter(user=user, product=product).exists():
            Review.objects.create(
                user=user,
                product=product,
                rating=random.randint(3, 5),
                title=random.choice(['Tuyệt vời', 'Thơm lắm', 'Tạm ổn', 'Chất lượng tốt']),
                comment='Sản phẩm dùng rất thích, đóng gói cẩn thận. Sẽ ủng hộ shop tiếp.'
            )
            # Update product rating
            reviews = Review.objects.filter(product=product)
            avg_rating = sum(r.rating for r in reviews) / len(reviews)
            product.rating = avg_rating
            product.num_reviews = len(reviews)
            product.save()

if __name__ == '__main__':
    create_users()
    cats = create_categories()
    create_products(cats)
    create_orders()
    create_reviews()
    print("Database seeding completed!")
