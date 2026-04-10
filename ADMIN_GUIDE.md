# Hướng Dẫn Sử Dụng Admin Panel

## 📌 Giới Thiệu

Hệ thống quản lý admin mới được xây dựng một cách chuyên nghiệp với các tính năng:
- **Dashboard** với thống kê chi tiết và biểu đồ
- **Quản lý sản phẩm** - Thêm, sửa, xóa sản phẩm
- **Quản lý đơn hàng** - Theo dõi và cập nhật trạng thái đơn hàng
- **Quản lý người dùng** - Xem thông tin khách hàng
- **Thống kê nâng cao** - Doanh thu, sản phẩm bán chạy, đánh giá
- **Biểu đồ tương tác** - Chart.js cho visualize dữ liệu

---

## 🔐 Cách Truy Cập

### Yêu Cầu
- Tài khoản **Admin** hoặc **Staff** trong Django
- Hoặc có role **admin** trong UserProfile

### URL Truy Cập
```
http://localhost:8000/admin-panel/
```

### Các URL Chính
- **Dashboard**: `/admin-panel/` hoặc `/admin-panel/dashboard/`
- **Sản Phẩm**: `/admin-panel/products/`
- **Đơn Hàng**: `/admin-panel/orders/`
- **Người Dùng**: `/admin-panel/users/`
- **Thống Kê**: `/admin-panel/statistics/`

---

## 📊 Dashboard

### Thông Tin Hiển Thị
1. **Thống Kê Cơ Bản** (4 Thẻ Chính)
   - Tổng người dùng
   - Tổng sản phẩm
   - Tổng đơn hàng
   - Tổng doanh thu

2. **Thống Kê Mở Rộng** (4 Thẻ Phụ)
   - Doanh thu tháng này
   - Tổng danh mục
   - Tổng đánh giá
   - Đơn chờ xác nhận

3. **Tình Trạng Đơn Hàng**
   - Chờ Xác Nhận (Vàng)
   - Đã Xác Nhận (Xanh Dương)
   - Đang Giao Hàng (Xanh Nước)
   - Hoàn Thành (Xanh Lá)

4. **Biểu Đồ**
   - **Biểu Đồ Doanh Thu & Đơn Hàng** (30 ngày gần đây)
     - Hiển thị doanh thu (trục Y trái) và số đơn hàng (trục Y phải)
   - **Biểu Đồ Tròn Danh Mục** - Phân bổ sản phẩm theo danh mục

5. **Bảng Dữ Liệu**
   - **Top 10 Sản Phẩm Bán Chạy** - Số lượng bán và doanh thu
   - **Danh Mục Sản Phẩm** - Top 8 danh mục
   - **Đơn Hàng Gần Đây** - 5 đơn hàng mới nhất

---

## 📦 Quản Lý Sản Phẩm

### Tính Năng
- ✅ Hiển thị danh sách sản phẩm với phân trang (20 items/trang)
- ✅ Tìm kiếm theo tên sản phẩm hoặc thương hiệu
- ✅ Lọc theo danh mục
- ✅ Xem chi tiết, chỉnh sửa, xóa sản phẩm

### Cột Dữ Liệu
| Cột | Mô Tả |
|-----|-------|
| Mã ID | ID sản phẩm |
| Tên Sản Phẩm | Tên và thương hiệu |
| Danh Mục | Danh mục sản phẩm |
| Giá | Giá bán (VNĐ) |
| Số Lượng | Tồn kho |
| Trạng Thái | Hoạt động/Ẩn |
| Ngày Tạo | Ngày tạo sản phẩm |
| Hành Động | Chi tiết, Chỉnh sửa, Xóa |

### Hành Động
```
🔍 Chi tiết - Xem thông tin chi tiết
✏️  Chỉnh sửa - Cập nhật sản phẩm
🗑️  Xóa - Xóa khỏi hệ thống
```

---

## 🛒 Quản Lý Đơn Hàng

### Tính Năng
- ✅ Hiển thị tất cả đơn hàng với phân trang
- ✅ Lọc theo trạng thái
- ✅ Xem chi tiết đơn hàng
- ✅ Cập nhật trạng thái đơn hàng

### Trạng Thái Đơn Hàng
| Trạng Thái | Màu | Mô Tả |
|-----------|-----|-------|
| Chờ Xác Nhận | Vàng | Đơn vừa được tạo |
| Đã Xác Nhận | Xanh Dương | Đã xác nhận thanh toán |
| Đang Giao Hàng | Xanh Nước | Đang vận chuyển |
| Hoàn Thành | Xanh Lá | Khách đã nhận hàng |
| Hủy Bỏ | Đỏ | Đơn hàng bị hủy |

### Chi Tiết Đơn Hàng
Khi nhấn "Chi Tiết", bạn sẽ thấy:
- **Thông Tin Khách Hàng**: Tên, Email, Phone, Địa chỉ
- **Thông Tin Đơn Hàng**: Mã đơn, ngày tạo, trạng thái
- **Danh Sách Sản Phẩm**: Tên, số lượng, giá, thành tiền
- **Tổng Tiền**: Tính toán toàn bộ giá trị
- **Thanh Toán**: Phương thức & trạng thái thanh toán
- **Cập Nhật Trạng Thái**: Form để thay đổi trạng thái

---

## 👥 Quản Lý Người Dùng

### Tính Năng
- ✅ Hiển thị danh sách người dùng
- ✅ Tìm kiếm theo tên, email
- ✅ Lọc theo vai trò (Admin/User)
- ✅ Xem chi tiết người dùng
- ✅ Phân trang (20 items/trang)

### Cột Dữ Liệu
| Cột | Mô Tả |
|-----|-------|
| Tên Người Dùng | Username |
| Email | Email địa chỉ |
| Họ Tên | Tên đầy đủ |
| Điện Thoại | Số điện thoại |
| Vai Trò | Admin hoặc User |
| Ngày Tham Gia | Ngày đăng ký |

### Chi Tiết Người Dùng
- **Thông Tin Cá Nhân**: Tên, email, điện thoại, địa chỉ
- **Thông Tin Liên Hệ**: Thành phố, tỉnh, mã bưu điện
- **Thống Kê**: Tổng tiền chi, số đơn hàng, điểm thành viên
- **Lịch Sử Đơn Hàng**: 10 đơn hàng gần đây của khách

---

## 📈 Thống Kê Chi Tiết

### Biểu Đồ Doanh Thu
- **Biểu Đồ Cột**: Doanh thu 12 tháng gần đây
- **Biểu Đồ Ngang**: Doanh thu theo danh mục
- **Biểu Đồ Tròn**: Tỷ lệ đơn hàng (Hoàn thành/Giao/Xác nhận/Chờ/Hủy)

### Sản Phẩm Được Đánh Giá Cao
- Hiển thị top 10 sản phẩm có rating cao nhất
- Số lượng đánh giá
- Điểm trung bình (1-5 sao)
- Mức độ : Xuất Sắc/Tốt/Bình Thường/Cần Cải Thiện

---

## 🎨 Giao Diện & Tính Năng

### Sidebar Menu
```
├── 📊 Dashboard
├── 📈 Thống Kê
├── 📦 Sản Phẩm
├── 🛒 Đơn Hàng
├── 👥 Người Dùng
├── 🏠 Về Trang Chủ
└── 🔓 Đăng Xuất
```

### Topbar
- Hiển thị tên trang
- Tên người dùng đăng nhập
- Nút Đăng Xuất

### Responsive Design
- ✅ Responsive trên mobile (sidebar thu nhỏ)
- ✅ Sidebar rộng trên desktop
- ✅ Các biểu đồ tự động điều chỉnh

---

## 🔒 Bảo Mật

### Yêu Cầu Quyền Hạn
- Chỉ Admin hoặc Staff mới có thể truy cập
- Decorator `@login_required` - Bắt đăng nhập
- Decorator `@user_passes_test(is_admin)` - Kiểm tra quyền admin

### Kiểm Tra Quyền
```python
def is_admin(user):
    return user.is_staff or (hasattr(user, 'profile') and user.profile.is_admin())
```

---

## 📋 Các Trường Dữ Liệu

### Product
- `name` - Tên sản phẩm
- `category` - Danh mục
- `description` - Mô tả
- `price` - Giá bán
- `discount_price` - Giá khuyến mãi
- `stock` - Số lượng tồn kho
- `brand` - Thương hiệu
- `is_active` - Trạng thái hoạt động

### Order
- `order_number` - Mã đơn
- `full_name` - Tên khách
- `email` - Email
- `phone` - Điện thoại
- `address` - Địa chỉ giao hàng
- `total_price` - Tổng tiền
- `final_price` - Giá cuối cùng
- `status` - Trạng thái
- `payment_method` - Phương thức thanh toán
- `is_paid` - Trạng thái thanh toán

### UserProfile
- `user` - Tài khoản Django
- `role` - Vai trò (guest/user/admin)
- `phone` - Điện thoại
- `address` - Địa chỉ
- `loyalty_points` - Điểm thành viên

---

## 📞 Hỗ Trợ & Liên Hệ

Nếu có vấn đề hoặc câu hỏi, vui lòng liên hệ với đội phát triển.

**Tạo ngày**: 17/02/2026
**Phiên bản**: 1.0
**Tác giả**: Admin Team
