from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum, Count, Q, Avg
from django.utils import timezone
from datetime import timedelta, datetime
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from products.models import Product, Category
from products.forms import ProductForm
from orders.models import Order, OrderDetail
from accounts.models import UserProfile
from reviews.models import Review
import json


def is_admin(user):
    """Kiểm tra người dùng có phải admin không"""
    return user.is_staff or (hasattr(user, 'profile') and user.profile.is_admin())


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def admin_dashboard(request):
    """Admin dashboard với thống kê chi tiết Status: Dashboard"""
    print(f"DEBUG: Rendering Dashboard for {request.user}")
    # Thống kê cơ bản
    total_users = UserProfile.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_categories = Category.objects.count()
    total_reviews = Review.objects.count()
    
    # Doanh thu
    total_revenue = Order.objects.filter(status='completed').aggregate(Sum('final_price'))['final_price__sum'] or 0
    this_month_revenue = Order.objects.filter(
        status='completed',
        created_at__month=timezone.now().month,
        created_at__year=timezone.now().year
    ).aggregate(Sum('final_price'))['final_price__sum'] or 0
    
    # Đơn hàng theo trạng thái
    pending_orders = Order.objects.filter(status='pending').count()
    approved_orders = Order.objects.filter(status='approved').count()
    shipped_orders = Order.objects.filter(status='shipped').count()
    completed_orders = Order.objects.filter(status='completed').count()
    cancelled_orders = Order.objects.filter(status='cancelled').count()
    
    # Sản phẩm bán chạy
    top_products = OrderDetail.objects.values('product__name', 'product__id').annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum('product_price')
    ).order_by('-total_quantity')[:10]
    
    # Thống kê 30 ngày gần đây
    daily_revenue = []
    daily_orders = []
    dates_labels = []
    
    for i in range(30):
        date = timezone.now() - timedelta(days=(29-i))
        start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        dates_labels.append(date.strftime('%d/%m'))
        
        revenue = Order.objects.filter(
            status='completed',
            created_at__gte=start,
            created_at__lt=end
        ).aggregate(Sum('final_price'))['final_price__sum'] or 0
        
        orders_count = Order.objects.filter(
            created_at__gte=start,
            created_at__lt=end
        ).count()
        
        daily_revenue.append(int(revenue))
        daily_orders.append(orders_count)
    
    # Sản phẩm theo danh mục
    category_products = Category.objects.annotate(product_count=Count('products')).order_by('-product_count')[:8]
    
    # Đơn hàng gần đây
    recent_orders = Order.objects.all().order_by('-created_at')[:5]
    
    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_categories': total_categories,
        'total_reviews': total_reviews,
        'total_revenue': int(total_revenue),
        'this_month_revenue': int(this_month_revenue),
        'pending_orders': pending_orders,
        'approved_orders': approved_orders,
        'shipped_orders': shipped_orders,
        'completed_orders': completed_orders,
        'cancelled_orders': cancelled_orders,
        'top_products': list(top_products),
        'category_products': category_products,
        'daily_revenue': json.dumps(daily_revenue),
        'daily_orders': json.dumps(daily_orders),
        'dates_labels': json.dumps(dates_labels),
        'recent_orders': recent_orders,
    }
    return render(request, 'admin/dashboard.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def admin_products(request):
    """Quản lý sản phẩm Status: Products"""
    print(f"DEBUG: Rendering Products for {request.user}")
    products = Product.objects.all().order_by('-created_at')
    
    # Tìm kiếm
    search = request.GET.get('search', '')
    if search:
        products = products.filter(Q(name__icontains=search) | Q(brand__icontains=search))
    
    # Lọc theo danh mục
    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category_id=category_filter)
    
    # Phân trang
    paginator = Paginator(products, 20)
    page = request.GET.get('page', 1)
    products = paginator.get_page(page)
    
    context = {
        'products': products,
        'categories': Category.objects.all(),
        'search': search,
        'category_filter': int(category_filter) if category_filter else None,
    }
    return render(request, 'admin/products.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def admin_orders(request):
    """Quản lý đơn hàng Status: Orders"""
    print(f"DEBUG: Rendering Orders for {request.user}")
    orders = Order.objects.all().order_by('-created_at')
    selected_status = request.GET.get('status', '')
    if selected_status:
        orders = orders.filter(status=selected_status)
    
    # Phân trang
    paginator = Paginator(orders, 20)
    page = request.GET.get('page', 1)
    orders = paginator.get_page(page)
    
    context = {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'selected_status': selected_status,
    }
    return render(request, 'admin/orders.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def admin_order_detail(request, order_id):
    """Chi tiết đơn hàng"""
    order = get_object_or_404(Order, id=order_id)
    order_details = order.details.all()
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'Cập nhật trạng thái đơn hàng thành: {order.get_status_display_vn()}')
            return redirect('admin_order_detail', order_id=order_id)
    
    context = {
        'order': order,
        'order_details': order_details,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'admin/order_detail.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def admin_users(request):
    """Quản lý người dùng Status: Users"""
    print(f"DEBUG: Rendering Users for {request.user}")
    users = UserProfile.objects.all().order_by('-created_at')
    
    # Tìm kiếm
    search = request.GET.get('search', '')
    if search:
        users = users.filter(Q(user__username__icontains=search) | 
                           Q(user__email__icontains=search) |
                           Q(user__first_name__icontains=search))
    
    # Lọc theo vai trò
    role_filter = request.GET.get('role')
    if role_filter:
        users = users.filter(role=role_filter)
    
    # Phân trang
    paginator = Paginator(users, 20)
    page = request.GET.get('page', 1)
    users = paginator.get_page(page)
    
    context = {
        'users': users,
        'role_choices': UserProfile.ROLE_CHOICES,
        'search': search,
        'role_filter': role_filter,
    }
    return render(request, 'admin/users.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def admin_user_detail(request, user_id):
    """Chi tiết người dùng"""
    user_profile = get_object_or_404(UserProfile, id=user_id)
    user = user_profile.user
    user_orders = user.orders.all().order_by('-created_at')
    
    context = {
        'user_profile': user_profile,
        'user': user,
        'user_orders': user_orders[:10],
        'total_spent': sum([order.final_price for order in user_orders if order.status == 'completed']),
    }
    return render(request, 'admin/user_detail.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def admin_statistics(request):
    """Thống kê chi tiết"""
    # Doanh thu theo tháng
    monthly_revenue = []
    monthly_labels = []
    
    for i in range(12):
        month = timezone.now().month - (11 - i)
        year = timezone.now().year
        
        if month <= 0:
            month += 12
            year -= 1
        
        revenue = Order.objects.filter(
            status='completed',
            created_at__month=month,
            created_at__year=year
        ).aggregate(Sum('final_price'))['final_price__sum'] or 0
        
        monthly_revenue.append(int(revenue))
        monthly_labels.append(f"T{month}/{year}")
    
    # Doanh thu theo danh mục
    category_revenue = []
    category_labels = []
    
    categories = Category.objects.annotate(
        revenue=Sum('products__orderdetail__order__final_price'),
        count=Count('products')
    ).order_by('-revenue')
    
    for category in categories:
        if category.revenue:
            category_labels.append(category.name)
            category_revenue.append(int(category.revenue or 0))
    
    # Tỷ lệ đơn hàng hoàn thành
    total_orders_count = Order.objects.count()
    order_status_data = {
        'completed': Order.objects.filter(status='completed').count(),
        'shipped': Order.objects.filter(status='shipped').count(),
        'approved': Order.objects.filter(status='approved').count(),
        'pending': Order.objects.filter(status='pending').count(),
        'cancelled': Order.objects.filter(status='cancelled').count(),
    }
    
    # Sản phẩm nhiều rating nhất
    top_rated = Product.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).filter(review_count__gt=0).order_by('-avg_rating')[:10]
    
    context = {
        'monthly_revenue': json.dumps(monthly_revenue),
        'monthly_labels': json.dumps(monthly_labels),
        'category_revenue': json.dumps(category_revenue),
        'category_labels': json.dumps(category_labels),
        'order_status_data': json.dumps(order_status_data),
        'top_rated': top_rated,
    }
    return render(request, 'admin/statistics.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_product_add(request):
    """Thêm sản phẩm mới"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Đã thêm sản phẩm {product.name} thành công.')
            return redirect('admin_products')
    else:
        form = ProductForm()
    
    return render(request, 'admin/product_form.html', {
        'form': form,
        'title': 'Thêm sản phẩm mới'
    })


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_product_edit(request, product_id):
    """Chỉnh sửa sản phẩm"""
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Đã cập nhật sản phẩm {product.name} thành công.')
            return redirect('admin_products')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'admin/product_form.html', {
        'form': form,
        'title': f'Chỉnh sửa: {product.name}',
        'product': product
    })


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_product_delete(request, product_id):
    """Xóa sản phẩm"""
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Đã xóa sản phẩm {product_name}.')
        return redirect('admin_products')
    
    return render(request, 'admin/product_confirm_delete.html', {'product': product})
