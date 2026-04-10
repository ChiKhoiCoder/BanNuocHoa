# TÓMLƯỢC CHỨC NĂNG CỦA PERFUME SHOP

## 📦 PACKAGE CỦA DỰ ÁN

Dự án này hiện đã có đủ 9 files chính cho Django project:

### 1. **accounts/** - Quản Lý Tài Khoản
```
✅ models.py          - UserProfile model với role (guest/user/admin)
✅ views.py           - Register, Login, Logout, Profile, Change Password
✅ forms.py           - UserRegistrationForm, UserLoginForm, UserProfileForm
✅ urls.py            - Routes cho authentication
✅ admin.py           - Django Admin interface
```

### 2. **products/** - Quản Lý Sản Phẩm & Giỏ Hàng
```
✅ models.py          - Category, Product, Cart, CartItem
✅ views.py           - Product CRUD, Search, Cart management
✅ forms.py           - ProductForm, CategoryForm, ProductSearchForm
✅ urls.py            - Routes cho sản phẩm
✅ admin.py           - Django Admin interface
✅ admin_views.py     - Admin Dashboard with statistics
✅ admin_urls.py      - Routes cho admin panel
✅ context_processors.py - Cart context cho templates
```

### 3. **orders/** - Quản Lý Đơn Hàng
```
✅ models.py          - Order, OrderDetail
✅ views.py           - Checkout, Order management, Order history
✅ forms.py           - CheckoutForm
✅ urls.py            - Routes cho orders
✅ admin.py           - Django Admin interface
```

### 4. **reviews/** - Quản Lý Đánh Giá
```
✅ models.py          - Review model (1-5 stars)
✅ views.py           - Add/Delete review
✅ forms.py           - ReviewForm
✅ urls.py            - Routes cho reviews
✅ admin.py           - Django Admin interface
```

### 5. **perfume_shop/** - Cấu Hình Project
```
✅ settings.py        - Django configuration
✅ urls.py            - Main URL router
✅ wsgi.py            - WSGI configuration
```

### 6. **templates/** - Giao Diện người Dùng
```
✅ base.html                           - Base template
✅ accounts/register.html              - Trang đăng ký
✅ accounts/login.html                 - Trang đăng nhập  
✅ accounts/profile.html               - Trang profile
✅ accounts/change_password.html       - Trang đổi mật khẩu
✅ products/home.html                  - Trang chủ
✅ products/product_list.html          - Danh sách sản phẩm
✅ products/product_detail.html        - Chi tiết sản phẩm
✅ products/product_card.html          - Component card sản phẩm
✅ products/category_list.html         - Danh mục sản phẩm
✅ products/category_detail.html       - Chi tiết danh mục
✅ products/cart.html                  - Giỏ hàng
✅ orders/checkout.html                - Trang thanh toán
✅ orders/order_confirmation.html      - Xác nhận đơn hàng
✅ orders/order_list.html              - Lịch sử đơn hàng
✅ orders/order_detail.html            - Chi tiết đơn hàng
✅ reviews/review_form.html            - Form viết đánh giá
✅ admin/dashboard.html                - Admin Dashboard
✅ admin/products.html                 - Admin quản lý sản phẩm
✅ admin/orders.html                   - Admin quản lý đơn hàng
✅ admin/users.html                    - Admin quản lý người dùng
```

---

## ✨ CÁC TÍNH NĂNG CHÍNH

### 🔐 Xác Thực & Phân Quyền
- ✅ Đăng ký tài khoản mới
- ✅ Đăng nhập / Đăng xuất
- ✅ Đổi mật khẩu
- ✅ Phân quyền: Guest, User, Admin
- ✅ Profile người dùng

### 🛍️ Quản Lý Sản Phẩm (CRUD)
- ✅ Thêm sản phẩm mới
- ✅ Sửa thông tin sản phẩm
- ✅ Xóa sản phẩm
- ✅ Hiển thị danh sách sản phẩm
- ✅ Tìm kiếm sản phẩm theo tên, brand, mô tả
- ✅ Lọc theo danh mục
- ✅ Lọc theo giá (min/max)
- ✅ Upload ảnh sản phẩm
- ✅ Kiểm tra dung lượng file
- ✅ Kiểm tra định dạng file

### 🛒 Giỏ Hàng & Đặt Hàng
- ✅ Thêm sản phẩm vào giỏ hàng
- ✅ Cập nhật số lượng
- ✅ Xóa sản phẩm khỏi giỏ
- ✅ Xóa toàn bộ giỏ hàng
- ✅ Tính tổng giá giỏ hàng
- ✅ Thanh toán (checkout)
- ✅ Tạo đơn hàng
- ✅ Lưu thông tin giao hàng

### 📋 Quản Lý Đơn Hàng
- ✅ Xem danh sách đơn hàng
- ✅ Xem chi tiết đơn hàng
- ✅ Cập nhật trạng thái (pending → approved → shipped → completed)
- ✅ Hủy đơn hàng
- ✅ Giá trị trạng thái: pending, approved, shipped, completed, cancelled
- ✅ Quản lý chi tiết đơn hàng

### ⭐ Đánh Giá Sản Phẩm
- ✅ Viết đánh giá (1-5 sao)
- ✅ Sửa đánh giá
- ✅ Xóa đánh giá
- ✅ Hiển thị tất cả đánh giá
- ✅ Cập nhật rating sản phẩm tự động

### 📊 Báo Cáo & Thống Kê
- ✅ Biểu đồ doanh thu 7 ngày (Line Chart)
- ✅ Biểu đồ số đơn hàng 7 ngày (Bar Chart)
- ✅ Biểu đồ trạng thái đơn hàng (Doughnut)
- ✅ Biểu đồ sản phẩm theo danh mục (Bar Chart)
- ✅ Thống kê tổng doanh thu
- ✅ Thống kê tổng đơn hàng
- ✅ Thống kê sản phẩm bán chạy (Top 5)
- ✅ Thống kê danh mục

### 🎯 Danh Mục
- ✅ Tạo danh mục sản phẩm
- ✅ Sửa danh mục
- ✅ Xóa danh mục
- ✅ Upload ảnh danh mục
- ✅ Hiển thị sản phẩm theo danh mục

---

## 🗄️ CÁC BẢNG DỮ LIỆU (9 BẢNG)

1. **auth_user** - Người dùng Django
2. **accounts_userprofile** - Hồ sơ người dùng mở rộng
3. **products_category** - Danh mục sản phẩm
4. **products_product** - Sản phẩm nước hoa
5. **products_cart** - Giỏ hàng
6. **products_cartitem** - Chi tiết giỏ hàng
7. **orders_order** - Đơn hàng
8. **orders_orderdetail** - Chi tiết đơn hàng
9. **reviews_review** - Đánh giá sản phẩm

---

## 🔧 CÁC CÔNG CỤ & THƯ VIỆN

### Backend
- Python 3.8+
- Django 4.2.7
- Django ORM
- Django Authentication

### Frontend
- Bootstrap 5.3
- HTML5
- CSS3
- JavaScript

### Charts & Visualization
- Chart.js 3.9.1

### File Upload
- Pillow (Python Imaging Library)

### Database
- SQLite (Development)
- MySQL/PostgreSQL (Production)

---

## 🎨 GIAO DIỆN ĐẶC ĐIỂM

- 🌟 Responsive design (Mobile-friendly)
- 🎨 Màu sắc chuyên nghiệp cho nước hoa
- 📱 Navigation menu với cart badge
- 🔍 Search và filter functions
- 📊 Dashboard thống kê động
- 🎓 User-friendly interface
- ⚡ Bootstrap framework for styling

---

## 📈 YÊU CẦU ĐƯỢC ĐÁP ỨNG

| Yêu Cầu | Status | Chi Tiết |
|---------|--------|---------|
| 5+ Bảng dữ liệu | ✅ | 9 bảng chính |
| 6+ Chức năng động | ✅ | 15+ chức năng |
| 2 Biểu đồ thống kê | ✅ | 4 biểu đồ |
| Upload file | ✅ | Hình ảnh sản phẩm, avatar, danh mục |
| Phân quyền | ✅ | Guest, User, Admin |
| Phân chia file nhỏ | ✅ | 20+ files Python và HTML |

---

## 🚀 HƯỚNG DẪN NHANH

### Cài Đặt
```bash
# 1. Tạo virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Cài dependencies
pip install -r requirements.txt

# 3. Tạo database
python manage.py migrate

# 4. Tạo dữ liệu mẫu
python manage.py seed_data

# 5. Chạy server
python manage.py runserver
```

### Truy Cập
- Website: http://localhost:8000
- Admin: http://localhost:8000/admin
- Dashboard: http://localhost:8000/admin-dashboard/dashboard/

### Tài Khoản Mẫu
- Admin: admin / admin123456
- User: user1 / user123456

---

## 🎓 HỌC TẬP TỪTƯƠNG

Dự án này là một ví dụ hoàn chỉnh về:
- Django project structure
- Model relationship (OneToOne, ForeignKey, ManyToMany)
- Authentication & Authorization
- Form handling & validation
- Template rendering
- Admin customization
- Static files & media management
- Database design
- URL routing
- Chart.js integration
- Bootstrap responsive design

---

**Dự Án Hoàn Tất! 🎉**

Bạn có thể bắt đầu sử dụng ngay bằng cách làm theo hướng dẫn trong INSTALL.md
