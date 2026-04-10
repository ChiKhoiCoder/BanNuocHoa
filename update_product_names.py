import os
import django

# Setup Django atmosphere
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'perfume_shop.settings')
django.setup()

from products.models import Product

def update_product_names():
    replacements = {
        "Chanel No.5": "Chanel No.5 - Biểu Tượng Sắc Đẹp Vĩnh Cửu",
        "Dior Sauvage": "Dior Sauvage - Bản Lĩnh Quý Ông Hiện Đại",
        "Gucci Bloom": "Gucci Bloom - Khu Vườn Hương Hoa Thuần Khiết",
        "Bleu de Chanel": "Bleu de Chanel - Sự Tự Do & Quyền Lực",
        "YSL Libre": "YSL Libre - Bản Tuyên Ngôn Của Sự Tự Do",
        "Lancôme La Vie Est Belle": "Lancôme La Vie Est Belle - Cuộc Sống Tươi Đẹp",
        "Versace Eros": "Versace Eros - Vị Thần Tình Yêu Đương Đại",
        "Armani Acqua di Gio": "Acqua di Gio - Tinh Túy Từ Đại Dương",
        "Tom Ford Black Orchid": "Black Orchid - Sự Quyến Rũ Huyền Bí",
        "Creed Aventus": "Creed Aventus - Khát Vọng Chinh Phục",
        "Marc Jacobs Daisy": "Marc Jacobs Daisy - Nét Ngây Thơ Rạng Rỡ",
        "Jean Paul Gaultier Le Male": "Le Male - Ngôi Sao Của Những Đại Dương",
        "Viktor & Rolf Flowerbomb": "Flowerbomb - Sự Bùng Nổ Của Hương Hoa",
        "Carolina Herrera Good Girl": "Good Girl - Nét Độc Bản Đầy Kiêu Hãnh",
        "Paco Rabanne 1 Million": "1 Million - Đỉnh Cao Của Sự Sang Trọng"
    }

    count = 0
    for old_name, new_name in replacements.items():
        products = Product.objects.filter(name__icontains=old_name)
        for p in products:
            p.name = new_name
            p.save()
            count += 1
            print(f"Updated: {old_name} -> {new_name}")

    print(f"\nTotal products updated: {count}")

if __name__ == "__main__":
    update_product_names()
