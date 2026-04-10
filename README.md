# Website Bán Nước Hoa Trực Tuyến - Perfume Shop

Một ứng dụng e-commerce hoàn chỉnh xây dựng bằng Django, cho phép người dùng xem sản phẩm, đặt hàng, thanh toán và quản lý đơn hàng của họ.

## 📋 Mục Lục

- [Tính Năng](#tính-năng)
- [Công Nghệ](#công-nghệ)
- [Cài Đặt](#cài-đặt)
- [Cách Sử Dụng](#cách-sử-dụng)
- [Cấu Trúc Project](#cấu-trúc-project)
- [API Endpoints](#api-endpoints)

## ✨ Tính Năng

### Cho Khách Hàng (Guest)
- ✅ Xem danh sách sản phẩm
- ✅ Tìm kiếm và lọc sản phẩm
- ✅ Xem chi tiết sản phẩm
- ✅ Đăng ký tài khoản
- ✅ Đăng nhập

### Cho Người Dùng (User)
- ✅ Đăng nhập / Đăng xuất
- ✅ Cập nhật thông tin cá nhân
- ✅ Thêm sản phẩm vào giỏ hàng
- ✅ Xem và quản lý giỏ hàng
- ✅ Đặt hàng (checkout)
- ✅ Xem lịch sử đơn hàng
- ✅ Viết và quản lý đánh giá sản phẩm
- ✅ Hủy đơn hàng

### Cho Admin
- ✅ Quản lý sản phẩm (CRUD)
- ✅ Quản lý danh mục
- ✅ Quản lý đơn hàng
- ✅ Quản lý người dùng
- ✅ Xem thống kê doanh thu
- ✅ Xem thống kê đơn hàng
- ✅ Xem sản phẩm bán chạy
- ✅ Dashboard với biểu đồ

## 🛠️ Công Nghệ

- **Backend**: Django 4.2.7
- **Database**: SQLite (Demo), MySQL/PostgreSQL (Production)
- **Frontend**: HTML5, CSS3, Bootstrap 5.3
- **Charts**: Chart.js
- **Storage**: File uploads with Pillow

## 📦 Cài Đặt

### Yêu Cầu
- Python 3.8+
- pip
- virtualenv (optional but recommended)

### Các Bước Cài Đặt

#### 1. Clone Project
```bash
git clone <repository-url>
cd perfume_shop
```

#### 2. Tạo Virtual Environment
```bash
python -m venv venv

# Trên Windows
venv\Scripts\activate

# Trên Linux/Mac
source venv/bin/activate
```

#### 3. Cài Đặt Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Tạo Migrations
```bash
python manage.py makemigrations
```

#### 5. Chạy Migrations
```bash
python manage.py migrate
```

#### 6. Tạo Dữ Liệu Mẫu (Tùy Chọn)
```bash
python populate_db.py
```

#### 7. Tạo Superuser (Admin)
```bash
python manage.py createsuperuser
```

#### 8. Chạy Development Server
```bash
python manage.py runserver
```

Mở trình duyệt và truy cập: http://localhost:8000

## 🚀 Cách Sử Dụng

### Tài Khoản Mẫu (Nếu Chạy `seed_data`)

**Admin Account:**
- Username: `admin`
- Password: `admin123456`

**User Account 1:**
- Username: `user1`
- Password: `user123456`

**User Account 2:**
- Username: `user2`
- Password: `user123456`

### Truy Cập Các Trang Chính

| Trang | URL | Mô Tả |
|-------|-----|-------|
| Trang Chủ | http://localhost:8000/ | Trang chủ |
| Sản Phẩm | http://localhost:8000/products/ | Danh sách sản phẩm |
| Giỏ Hàng | http://localhost:8000/cart/ | Xem giỏ hàng |
| Thanh Toán | http://localhost:8000/orders/checkout/ | Trang thanh toán |
| Đơn Hàng | http://localhost:8000/orders/orders/ | Lịch sử đơn hàng |
| Admin | http://localhost:8000/admin/ | Admin Panel |
| Dashboard | http://localhost:8000/admin-dashboard/dashboard/ | Admin Dashboard |

## 📁 Cấu Trúc Project

```
perfume_shop/
│
├── accounts/                 # Quản lý tài khoản người dùng
│   ├── models.py            # UserProfile model
│   ├── views.py             # Authentication views
│   ├── forms.py             # User forms
│   ├── urls.py              # Account URLs
│   └── admin.py             # Admin interface
│
├── products/                # Quản lý sản phẩm
│   ├── models.py            # Product, Category, Cart models
│   ├── views.py             # Product views
│   ├── admin_views.py       # Admin views
│   ├── forms.py             # Product forms
│   ├── urls.py              # Product URLs
│   ├── admin_urls.py        # Admin URLs
│   ├── context_processors.py # Template context
│   └── admin.py             # Admin interface
│
├── orders/                  # Quản lý đơn hàng
│   ├── models.py            # Order, OrderDetail models
│   ├── views.py             # Order views
│   ├── forms.py             # Order forms
│   ├── urls.py              # Order URLs
│   └── admin.py             # Admin interface
│
├── reviews/                 # Quản lý đánh giá
│   ├── models.py            # Review model
│   ├── views.py             # Review views
│   ├── forms.py             # Review forms
│   ├── urls.py              # Review URLs
│   └── admin.py             # Admin interface
│
├── perfume_shop/            # Project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URLs
│   ├── wsgi.py              # WSGI config
│   └── __init__.py
│
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── accounts/            # Account templates
│   ├── products/            # Product templates
│   ├── orders/              # Order templates
│   ├── admin/               # Admin templates
│   └── reviews/             # Review templates
│
├── static/                  # Static files
│   ├── css/                 # CSS files
│   ├── js/                  # JavaScript files
│   └── images/              # Images
│
├── media/                   # User uploads
│   └── products/            # Product images
│
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── README.md                # Documentation
```

## 🗄️ Cơ Sở Dữ Liệu

### Models Chính

#### 1. User (Django Auth)
- Username, Email, Password
- First Name, Last Name
- Is Staff, Is Superuser

#### 2. UserProfile
```python
- user (OneToOne → User)
- role (choices: guest, user, admin)
- phone, address, city, state, zip_code
- date_of_birth, avatar
- created_at, updated_at
```

#### 3. Category
```python
- name (unique)
- description
- image
- created_at, updated_at
```

#### 4. Product
```python
- name, category (FK), brand
- description, price, discount_price
- image, stock
- scent_type, volume
- rating, num_reviews
- is_featured, is_active
- created_at, updated_at
```

#### 5. Cart
```python
- user (OneToOne → User)
- created_at, updated_at
```

#### 6. CartItem
```python
- cart (FK), product (FK)
- quantity
- created_at, updated_at
```

#### 7. Order
```python
- user (FK), order_number (unique)
- full_name, email, phone
- address, city, state, zip_code
- total_price, shipping_cost, final_price
- payment_method, is_paid
- status (pending, approved, shipped, completed, cancelled)
- notes
- created_at, updated_at
```

#### 8. OrderDetail
```python
- order (FK), product (FK)
- product_name, product_price
- quantity
```

#### 9. Review
```python
- product (FK), user (FK)
- rating (1-5)
- title, comment
- is_approved
- created_at, updated_at
```

## 🔐 Phân Quyền

| Chức Năng | Guest | User | Admin |
|-----------|-------|------|-------|
| Xem sản phẩm | ✅ | ✅ | ✅ |
| Thêm vào giỏ | ❌ | ✅ | ✅ |
| Đặt hàng | ❌ | ✅ | ✅ |
| Xem đơn hàng | ❌ | ✅ | ✅ |
| Viết đánh giá | ❌ | ✅ | ✅ |
| Quản lý sản phẩm | ❌ | ❌ | ✅ |
| Quản lý đơn hàng | ❌ | ❌ | ✅ |
| Xem thống kê | ❌ | ❌ | ✅ |

## 📊 Thống Kê & Báo Cáo

### Dashboard Admin Bao Gồm:
- 📈 Biểu đồ doanh thu 7 ngày
- 📊 Biểu đồ số đơn hàng
- 🔶 Biểu đồ trạng thái đơn hàng (Doughnut)
- 📋 Top 5 sản phẩm bán chạy
- 📂 Phân bố sản phẩm theo danh mục
- 💰 Tổng doanh thu
- 👥 Tổng người dùng
- 📦 Tổng sản phẩm

## 🔗 API Endpoints

### Accounts
```
GET     /accounts/register/              - Trang đăng ký
POST    /accounts/register/              - Xử lý đăng ký
GET     /accounts/login/                 - Trang đăng nhập
POST    /accounts/login/                 - Xử lý đăng nhập
GET     /accounts/logout/                - Đăng xuất
GET     /accounts/profile/               - Xem profile
POST    /accounts/profile/               - Cập nhật profile
GET     /accounts/change-password/       - Trang đổi mật khẩu
POST    /accounts/change-password/       - Xử lý đổi mật khẩu
```

### Products
```
GET     /                                - Trang chủ
GET     /products/                       - Danh sách sản phẩm
GET     /products/<id>/                  - Chi tiết sản phẩm
GET     /categories/                     - Danh sách danh mục
GET     /categories/<id>/                - Chi tiết danh mục
GET     /cart/                           - Xem giỏ hàng
POST    /cart/add/<product_id>/          - Thêm vào giỏ
POST    /cart/update/<item_id>/          - Cập nhật giỏ
POST    /cart/remove/<item_id>/          - Xóa khỏi giỏ
POST    /cart/clear/                     - Xóa toàn bộ giỏ
```

### Orders
```
GET     /orders/checkout/                - Trang thanh toán
POST    /orders/checkout/                - Xử lý thanh toán
GET     /orders/confirmation/<order>/    - Xác nhận đơn hàng
GET     /orders/orders/                  - Danh sách đơn hàng
GET     /orders/orders/<order>/          - Chi tiết đơn hàng
POST    /orders/orders/<order>/cancel/   - Hủy đơn hàng
```

### Reviews
```
GET     /reviews/add/<product_id>/       - Trang viết đánh giá
POST    /reviews/add/<product_id>/       - Xử lý đánh giá
POST    /reviews/delete/<review_id>/     - Xóa đánh giá
```

### Admin
```
GET     /admin-dashboard/dashboard/      - Admin Dashboard
GET     /admin-dashboard/products/       - Quản lý sản phẩm
GET     /admin-dashboard/orders/         - Quản lý đơn hàng
GET     /admin-dashboard/users/          - Quản lý người dùng
GET     /admin/                          - Django Admin
```

## 🎯 Yêu Cầu Được Đáp Ứng

### Cơ Sở Dữ Liệu
- ✅ **5+ Bảng dữ liệu**: User, UserProfile, Category, Product, Cart, CartItem, Order, OrderDetail, Review
- ✅ **SQLite Database**: Dùng cho development

### Chức Năng Động
- ✅ Đăng ký / Đăng nhập
- ✅ CRUD sản phẩm (Admin)
- ✅ Giỏ hàng & Đặt hàng
- ✅ Quản lý đơn hàng
- ✅ Đánh giá sản phẩm
- ✅ Upload hình ảnh

### Biểu Đồ Thống Kê
- ✅ Biểu đồ doanh thu (Line Chart)
- ✅ Biểu đồ trạng thái đơn hàng (Doughnut Chart)

### Phân Quyền
- ✅ Guest: Xem sản phẩm
- ✅ User: Mua hàng, viết đánh giá
- ✅ Admin: Quản lý toàn bộ hệ thống

### Upload File
- ✅ Upload ảnh sản phẩm
- ✅ Upload ảnh đại diện người dùng
- ✅ Upload ảnh danh mục

## 🐛 Troubleshooting

### Lỗi: ModuleNotFoundError
**Giải pháp**: Chắc chắn virtual environment được activate:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Lỗi: Database Error
**Giải pháp**: Chạy migrations:
```bash
python manage.py migrate
```

### Lỗi: Static Files Not Found
**Giải pháp**: Thu thập static files:
```bash
python manage.py collectstatic --noinput
```

## 📝 Ghi Chú

- Admin panel có sẵn tại `/admin/`
- Dữ liệu mẫu có thể được tạo bằng command `seed_data`
- Tất cả hình ảnh được lưu trong thư mục `media/`
- Session timeout được cấu hình là 2 tuần

## 📞 Liên Hệ

- Email: info@perfumeshop.com
- Điện thoại: (+84) 123-456-789
- Địa chỉ: Hà Nội, Việt Nam

## 📜 License

MIT License - Tự do sử dụng cho mục đích học tập và thương mại.

---

**Phiên bản**: 1.0
**Ngày cập nhật**: 2024
