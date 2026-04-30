"""Script thêm các danh mục nước hoa vào database"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'perfume_shop.settings')
django.setup()

from products.models import Category

categories = [
    {
        'name': 'Nước Hoa Nam',
        'description': 'Bộ sưu tập nước hoa dành cho phái mạnh với hương thơm nam tính, lịch lãm và quyến rũ.',
    },
    {
        'name': 'Nước Hoa Nữ',
        'description': 'Nước hoa dành cho phái đẹp với hương thơm ngọt ngào, quyến rũ và sang trọng.',
    },
    {
        'name': 'Nước Hoa Unisex',
        'description': 'Hương thơm trung tính phù hợp cho cả nam và nữ, hiện đại và phá cách.',
    },
    {
        'name': 'Nước Hoa Cao Cấp',
        'description': 'Dòng nước hoa thượng hạng từ các thương hiệu danh tiếng thế giới như Chanel, Dior, Tom Ford.',
    },
    {
        'name': 'Nước Hoa Mini & Travel Size',
        'description': 'Chai nước hoa nhỏ gọn, tiện lợi mang theo khi du lịch hoặc dùng thử trước khi mua chai lớn.',
    },
    {
        'name': 'Set Quà Tặng',
        'description': 'Bộ quà tặng nước hoa kèm sản phẩm chăm sóc cơ thể, hoàn hảo cho dịp lễ và sinh nhật.',
    },
    {
        'name': 'Nước Hoa Ả Rập',
        'description': 'Tinh dầu nước hoa Ả Rập đậm đà, bền mùi với hương gỗ trầm, oud và xạ hương.',
    },
    {
        'name': 'Nước Hoa Niche',
        'description': 'Dòng nước hoa nghệ thuật độc đáo từ các nhà sáng tạo hương thơm hàng đầu.',
    },
]

count = 0
for cat_data in categories:
    obj, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={'description': cat_data['description']}
    )
    if created:
        count += 1
        print(f"  + Added: {obj.pk}")
    else:
        print(f"  - Exists: {obj.pk}")

print(f"\nDone! Added {count} new categories. Total: {Category.objects.count()}")
