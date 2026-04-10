from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Category, Product
from accounts.models import UserProfile
from reviews.models import Review
import random


class Command(BaseCommand):
    help = 'Tạo dữ liệu mẫu cho ứng dụng'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Bắt đầu tạo dữ liệu mẫu...'))
        
        # Tạo danh mục
        categories_data = [
            {'name': 'Nam', 'description': 'Nước hoa dành cho nam'},
            {'name': 'Nữ', 'description': 'Nước hoa dành cho nữ'},
            {'name': 'Unisex', 'description': 'Nước hoa unisex'},
            {'name': 'Premium', 'description': 'Nước hoa cao cấp'},
            {'name': 'Niche', 'description': 'Nước hoa niche'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = cat
            if created:
                self.stdout.write(f'Tạo danh mục: {cat.name}')
        
        # Tạo sản phẩm mẫu
        products_data = [
            {
                'name': 'Dior Sauvage',
                'category': 'Nam',
                'brand': 'Dior',
                'scent_type': 'EDT',
                'volume': '100ml',
                'price': 2500000,
                'discount_price': 2200000,
                'stock': 50,
                'description': 'Nước hoa nam nổi tiếng với mùi hương dịu dàng, nam tính. Phù hợp cho mọi dịp.',
                'is_featured': True,
            },
            {
                'name': 'Chanel No. 5',
                'category': 'Nữ',
                'brand': 'Chanel',
                'scent_type': 'EDP',
                'volume': '50ml',
                'price': 3500000,
                'discount_price': 3100000,
                'stock': 30,
                'description': 'Biểu tượng của sự sang trọng và tinh tế. Mùi hương kinh điển vượt thời gian.',
                'is_featured': True,
            },
            {
                'name': 'Guerlain La Petite Robe Noire',
                'category': 'Nữ',
                'brand': 'Guerlain',
                'scent_type': 'EDP',
                'volume': '100ml',
                'price': 3000000,
                'discount_price': None,
                'stock': 25,
                'description': 'Nước hoa nữ tinh tế với hương thơm cam quýt tươi mát.',
                'is_featured': True,
            },
            {
                'name': 'Tom Ford Tobacco Vanille',
                'category': 'Unisex',
                'brand': 'Tom Ford',
                'scent_type': 'EDP',
                'volume': '100ml',
                'price': 4500000,
                'discount_price': 3900000,
                'stock': 15,
                'description': 'Hương thơm ấm áp và tính cách. Với vanilla và thuốc lá là những nốt chính.',
                'is_featured': True,
            },
            {
                'name': 'Yves Saint Laurent Black Opium',
                'category': 'Nữ',
                'brand': 'YSL',
                'scent_type': 'EDP',
                'volume': '90ml',
                'price': 2800000,
                'discount_price': 2400000,
                'stock': 40,
                'description': 'Mùi hương bí ẩn, quyến rũ và mạnh mẽ cho phụ nữ hiện đại.',
                'is_featured': False,
            },
            {
                'name': 'Dolce & Gabbana Light Blue',
                'category': 'Nữ',
                'brand': 'Dolce & Gabbana',
                'scent_type': 'EDT',
                'volume': '100ml',
                'price': 1800000,
                'discount_price': 1500000,
                'stock': 60,
                'description': 'Nước hoa nữ tươi mát với mùi hương cam quýt và hoa lemon.',
                'is_featured': False,
            },
            {
                'name': 'Versace Eros',
                'category': 'Nam',
                'brand': 'Versace',
                'scent_type': 'EDT',
                'volume': '100ml',
                'price': 2200000,
                'discount_price': 1800000,
                'stock': 45,
                'description': 'Hương thơm nam lạnh lùng với nốt bạc hà và sô-cô-la.',
                'is_featured': False,
            },
            {
                'name': 'Marc Jacobs Daisy',
                'category': 'Nữ',
                'brand': 'Marc Jacobs',
                'scent_type': 'EDT',
                'volume': '100ml',
                'price': 1500000,
                'discount_price': 1200000,
                'stock': 70,
                'description': 'Nước hoa nữ tươi sáng, năng động với mùi hương hoa cúc tự nhiên.',
                'is_featured': False,
            },
            {
                'name': 'Creed Aventus',
                'category': 'Nam',
                'brand': 'Creed',
                'scent_type': 'EDP',
                'volume': '120ml',
                'price': 6000000,
                'discount_price': 5200000,
                'stock': 10,
                'description': 'Nước hoa nam cao cấp với hương thơm quý phái và lạnh lùng.',
                'is_featured': True,
            },
            {
                'name': 'Carlo Pazolini Noir',
                'category': 'Niche',
                'brand': 'Carlo Pazolini',
                'scent_type': 'EDP',
                'volume': '100ml',
                'price': 2000000,
                'discount_price': 1700000,
                'stock': 20,
                'description': 'Nước hoa niche với hương thơm đặc biệt và độc nhất.',
                'is_featured': False,
            },
        ]
        
        for prod_data in products_data:
            category = categories[prod_data.pop('category')]
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'category': category,
                    **prod_data,
                    'image': 'products/default.jpg'
                }
            )
            if created:
                self.stdout.write(f'Tạo sản phẩm: {product.name}')
        
        # Tạo người dùng mẫu
        users_data = [
            {
                'username': 'admin',
                'email': 'admin@perfumeshop.com',
                'password': 'admin123456',
                'is_staff': True,
                'is_superuser': True,
                'first_name': 'Quản',
                'last_name': 'Lý',
            },
            {
                'username': 'user1',
                'email': 'user1@perfumeshop.com',
                'password': 'user123456',
                'first_name': 'Nguyễn',
                'last_name': 'Văn A',
            },
            {
                'username': 'user2',
                'email': 'user2@perfumeshop.com',
                'password': 'user123456',
                'first_name': 'Trần',
                'last_name': 'Thị B',
            },
        ]
        
        for user_data in users_data:
            password = user_data.pop('password')
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            if created:
                user.set_password(password)
                user.save()
                # Tạo profile
                role = 'admin' if user.is_staff else 'user'
                UserProfile.objects.get_or_create(
                    user=user,
                    defaults={'role': role}
                )
                self.stdout.write(f'Tạo người dùng: {user.username}')
        
        # Tạo đánh giá mẫu
        samples_products = Product.objects.all()[:5]
        sample_users = User.objects.filter(username__in=['user1', 'user2'])
        
        for product in samples_products:
            for user in sample_users:
                Review.objects.get_or_create(
                    product=product,
                    user=user,
                    defaults={
                        'rating': random.randint(3, 5),
                        'title': f'Sản phẩm tốt',
                        'comment': f'Đây là một sản phẩm chất lượng tốt. Mùi hương thơm ngon và lâu lâu.',
                    }
                )
        
        self.stdout.write(self.style.SUCCESS('✓ Tạo dữ liệu mẫu thành công!'))
