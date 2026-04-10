# HƯỚNG DẪN CHẠY DỰ ÁN PERFUME SHOP

## 🚀 Các Bước Cài Đặt Nhanh

### 1. Chuẩn Bị Môi Trường

```bash
# Mở Command Prompt hoặc PowerShell
# Điều hướng đến thư mục project
cd d:\Virual Code 2022\Project_BanNuocHoa\perfume_shop
```

### 2. Tạo Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Cài Đặt Dependencies

```bash
pip install -r requirements.txt
```

### 4. Tạo Database (Migrations)

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Tạo Dữ Liệu Mẫu (Tùy Chọn nhưng Khuyến Khích)

```bash
python manage.py seed_data
```

### 6. Tạo Tài Khoản Admin (Nếu Không Sử Dụng seed_data)

```bash
python manage.py createsuperuser
# Nhập username, email, password
```

### 7. Chạy Development Server

```bash
python manage.py runserver
```

Mở trình duyệt và truy cập: **http://localhost:8000**

---

## 🔑 Tài Khoản Đã Tạo (Nếu Chạy seed_data)

| Username | Password | Vai Trò |
|----------|----------|---------|
| admin | admin123456 | Admin |
| user1 | user123456 | User |
| user2 | user123456 | User |

---

## 🌐 URLs Quan Trọng

### Khách Hàng
- **Trang Chủ**: http://localhost:8000/
- **Danh Sách Sản Phẩm**: http://localhost:8000/products/
- **Danh Mục**: http://localhost:8000/categories/
- **Giỏ Hàng**: http://localhost:8000/cart/ (Cần đăng nhập)
- **Đăng Ký**: http://localhost:8000/accounts/register/
- **Đăng Nhập**: http://localhost:8000/accounts/login/

### Người Dùng Đã Đăng Nhập
- **Profile**: http://localhost:8000/accounts/profile/
- **Đơn Hàng**: http://localhost:8000/orders/orders/
- **Thanh Toán**: http://localhost:8000/orders/checkout/ (Cần có hàng trong giỏ)

### Admin
- **Admin Panel**: http://localhost:8000/admin/
- **Admin Dashboard**: http://localhost:8000/admin-dashboard/dashboard/
- **Quản Lý Sản Phẩm**: http://localhost:8000/admin-dashboard/products/
- **Quản Lý Đơn Hàng**: http://localhost:8000/admin-dashboard/orders/
- **Quản Lý Người Dùng**: http://localhost:8000/admin-dashboard/users/

---

## 📋 Các Bước Sử Dụng Chính

### 1️⃣ Mở Website
Truy cập: http://localhost:8000

### 2️⃣ Duyệt Sản Phẩm
- Klikck "Sản phẩm" hoặc "Danh mục" để xem các nước hoa
- Sử dụng tìm kiếm và lọc để tìm sản phẩm mong muốn

### 3️⃣ Đăng Ký/Đăng Nhập
- Nhấp "Đăng ký" để tạo tài khoản mới
- Hoặc "Đăng nhập" với tài khoản có sẵn

### 4️⃣ Thêm Vào Giỏ Hàng
- Xem chi tiết sản phẩm
- Chọn số lượng
- Nhấp "Thêm vào giỏ"

### 5️⃣ Thanh Toán
- Đi đến giỏ hàng
- Xem lại sản phẩm
- Nhấp "Thanh toán"
- Nhập thông tin giao hàng
- Chọn phương thức thanh toán
- Hoàn tất đơn hàng

### 6️⃣ Quản Lý Đơn Hàng
- Xem lịch sử đơn hàng
- Xem chi tiết từng đơn
- Hủy đơn hàng nếu cần

### 7️⃣ Viết Đánh Giá
- Xem sản phẩm đã mua
- Nhấp "Viết đánh giá"
- Cho 1-5 sao
- Viết bình luận
- Gửi đánh giá

---

## 🔧 Các Lệnh Useful

```bash
# Chạy development server
python manage.py runserver

# Chạy server trên port khác
python manage.py runserver 8080

# Tạo migrations
python manage.py makemigrations

# Chạy migrations
python manage.py migrate

# Tạo dữ liệu mẫu
python manage.py seed_data

# Tạo superuser
python manage.py createsuperuser

# Shell Django (Testing)
python manage.py shell

# Kiểm tra dependencies
pip list

# Cập nhật dependencies
pip install -r requirements.txt --upgrade
```

---

## 🎨 Tùy Chỉnh Giao Diện

### Thay Đổi Màu Sắc
File: `templates/base.html`
```css
:root {
    --primary-color: #d4a574;      /* Màu chính */
    --secondary-color: #8b7355;    /* Màu phụ */
    --dark-color: #2c2c2c;         /* Màu tối */
    --light-color: #f8f7f3;        /* Màu sáng */
}
```

### Thêm Logo
Thay thế phần logo trong `templates/base.html`:
```html
<a class="navbar-brand" href="{% url 'home' %}">
    <img src="/static/images/logo.png" alt="Logo">
    PERFUME SHOP
</a>
```

---

## 🐛 Xử Lý Lỗi Thường Gặp

### Lỗi: Python không được tìm thấy
**Giải pháp**: Cài đặt Python hoặc thêm vào PATH

### Lỗi: ModuleNotFoundError (django, pillow, etc.)
**Giải pháp**:
```bash
pip install -r requirements.txt
```

### Lỗi: Database không tồn tại
**Giải pháp**:
```bash
python manage.py migrate
```

### Lỗi: Port 8000 đã được sử dụng
**Giải pháp**:
```bash
python manage.py runserver 8080
# Hoặc tìm và kill process đang sử dụng port 8000
```

### Lỗi: Static files không hiển thị
**Giải pháp**:
```bash
python manage.py collectstatic --noinput
```

### Lỗi: Hình ảnh không tải được
**Giải pháp**: Kiểm tra thư mục `media/` tồn tại và có quyền ghi

---

## 📊 Kiểm Tra Dữ Liệu

### Qua Admin Panel
1. Tại http://localhost:8000/admin/
2. Đăng nhập bằng tài khoản admin
3. Xem các bảng: Users, Products, Orders, Categories

### Qua Django Shell
```bash
python manage.py shell
```

```python
# Kiểm tra sản phẩm
from products.models import Product
Product.objects.count()  # Số lượng sản phẩm

# Kiểm tra người dùng
from django.contrib.auth.models import User
User.objects.count()  # Số lượng người dùng

# Kiểm tra đơn hàng
from orders.models import Order
Order.objects.count()  # Số lượng đơn hàng
```

---

## 🔒 Bảo Mật

### Bước Chuẩn Bị Cho Production
1. Đổi `SECRET_KEY` trong `settings.py`
2. Setpoint `DEBUG = False`
3. Cấu hình `ALLOWED_HOSTS`
4. Sử dụng PostgreSQL thay SQLite
5. Bật HTTPS
6. Cấu hình email backend

### Tạo Requirements.txt Mới
```bash
pip freeze > requirements.txt
```

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra lại các bước cài đặt
2. Xem Django Documentation: https://docs.djangoproject.com/
3. Kiểm tra error messages trong terminal/console

---

**Chúc bạn thành công với dự án! 🎉**
