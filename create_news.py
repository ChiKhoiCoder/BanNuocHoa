import os
import django
import requests
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'perfume_shop.settings')
django.setup()

from products.models import NewsPost
from django.contrib.auth.models import User
from django.utils.text import slugify

def update_vivid_news():
    author = User.objects.filter(is_superuser=True).first()
    if not author:
        author = User.objects.create_user(username='admin_news', password='password123')
    
    # Delete old sample news
    NewsPost.objects.all().delete()
    
    news_data = [
        {
            'title': 'Thị trường Nước hoa Việt Nam 2026: Đẳng cấp và Sự khác biệt',
            'content': 'Năm 2026 chứng kiến sự bùng nổ của thị trường nước hoa xa xỉ tại Việt Nam. Người tiêu dùng Việt, đặc biệt là tại các thành phố lớn như Hà Nội và TP.HCM, ngày càng khắt khe hơn trong việc lựa chọn mùi hương biểu trưng cho cá tính riêng.\n\nXu hướng hiện nay không chỉ dừng lại ở các dòng Designer nổi tiếng mà đang chuyển dịch mạnh mẽ sang Niche Perfume - những kiệt tác mùi hương với nguyên liệu quý hiếm và số lượng giới hạn. Khách hàng sẵn sàng chi trả hàng chục triệu đồng cho một chai nước hoa có câu chuyện riêng và độ bám tỏa xuất sắc trong khí hậu nhiệt đới.',
            'image_url': 'https://images.unsplash.com/photo-1594035910387-fea47794261f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80'
        },
        {
            'title': 'Top 5 mùi hương "Signature" được quý ông Việt săn đón nhất',
            'content': 'Đối với phái mạnh Việt, nước hoa không chỉ là mùi hương mà còn là món phụ kiện khẳng định quyền lực và sự lịch lãm. Những tông hương Gỗ (Woody), Da thuộc (Leather) và Hổ phách (Amber) luôn giữ vững vị trí độc tôn trong các buổi tiệc tối thượng lưu.\n\nCác dòng sản phẩm như Tom Ford Ombré Leather, Creed Aventus hay Kilian Black Phantom đang tạo nên cơn sốt nhờ khả năng tạo ấn tượng mạnh mẽ ngay từ lần gặp đầu tiên. Chúng tôi ghi nhận sự tăng trưởng 40% doanh số cho các dòng nước hoa nam cao cấp trong quý đầu năm 2026.',
            'image_url': 'https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80'
        },
        {
            'title': 'Nghệ thuật sử dụng nước hoa trong khí hậu nóng ẩm tại Việt Nam',
            'content': 'Việc sử dụng nước hoa tại Việt Nam đòi hỏi sự tinh tế do đặc thù khí hậu nhiệt đới nóng và ẩm. Một mùi hương quá nồng có thể gây khó chịu cho đồng nghiệp hoặc người đi cùng.\n\nCác chuyên gia khuyên rằng: "Hãy ưu tiên các nốt hương Cam chanh (Citrus), Trà xanh (Green Tea) hoặc Biển cả (Aquatic) vào ban ngày". Ban đêm, bạn có thể thỏa sức với các tông hương quyến rũ hơn. Đừng quên xịt nước hoa lên quần áo hoặc các điểm có mạch đập để hương thơm lưu giữ bền bỉ nhất bất chấp mồ hôi và khói bụi.',
            'image_url': 'https://images.unsplash.com/photo-1547610291-eb6964147ac5?ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80'
        }
    ]

    for item in news_data:
        slug = slugify(item['title'])
        post = NewsPost.objects.create(
            title=item['title'],
            slug=slug,
            content=item['content'],
            author=author,
            is_published=True
        )
        
        # Download and save image
        try:
            response = requests.get(item['image_url'])
            if response.status_code == 200:
                img_name = f"{slug}.jpg"
                post.image.save(img_name, ContentFile(response.content), save=True)
                print(f"Saved image for: {item['title']}")
        except Exception as e:
            print(f"Error downloading image for {item['title']}: {e}")
            
        print(f"Created vivid news: {item['title']}")

if __name__ == '__main__':
    update_vivid_news()
