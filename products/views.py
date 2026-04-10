from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from .models import Product, Category, NewsPost, ContactMessage
from .models import NewsletterSubscriber
from .forms import ProductSearchForm, ProductForm, CategoryForm
# from .utils import get_cart  <- Removed
from reviews.models import Review
from .models import WishlistItem
from django.http import JsonResponse


def home(request):
    """Trang chủ - hiển thị sản phẩm nổi bật"""
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:6]
    # Exclude categories with empty or invalid pk
    categories = [c for c in Category.objects.all()[:10] if c.pk][:6]
    latest_products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    discounted_products = Product.objects.filter(is_active=True, discount_price__gt=0).order_by('?')[:4]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'latest_products': latest_products,
        'discounted_products': discounted_products,
    }
    return render(request, 'products/home.html', context)


def product_list(request):
    """Danh sách sản phẩm với tìm kiếm và lọc"""
    products = Product.objects.filter(is_active=True)
    
    # Lấy danh sách danh mục và thương hiệu để hiển thị trong sidebar
    categories = Category.objects.all()
    # Lấy các scent_type duy nhất
    scent_types = Product.objects.filter(is_active=True).exclude(scent_type='').values_list('scent_type', flat=True).distinct().order_by('scent_type')
    brands = Product.objects.filter(is_active=True).values_list('brand', flat=True).distinct().order_by('brand')
    
    # Tìm kiếm
    query = request.GET.get('query', '')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(brand__icontains=query)
        )
    
    # Lọc theo danh mục (nhiều danh mục)
    selected_categories = request.GET.getlist('category')
    if selected_categories:
        products = products.filter(category_id__in=selected_categories)
    
    # Lọc theo thương hiệu (nhiều thương hiệu)
    selected_brands = request.GET.getlist('brand')
    if selected_brands:
        products = products.filter(brand__in=selected_brands)

    # Lọc theo loại mùi hương (scent_type)
    selected_scents = request.GET.getlist('scent_type')
    if selected_scents:
        products = products.filter(scent_type__in=selected_scents)
    
    # Lọc theo tag (thay thế cho selected_tag cũ để đồng bộ với query)
    selected_tag = request.GET.get('tag')
    if selected_tag:
        products = products.filter(
            Q(name__icontains=selected_tag) | 
            Q(description__icontains=selected_tag) |
            Q(brand__icontains=selected_tag)
        )
    
    # Lọc khuyến mại
    is_sale = request.GET.get('sale')
    if is_sale == '1':
        products = products.filter(Q(discount_price__gt=0) | Q(flashsales__is_active=True)).distinct()
    
    # Lọc theo giá
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    price_range = request.GET.get('price_range')
    
    if price_range:
        # Giả sử price_range là giá trị max từ slider
        products = products.filter(price__lte=price_range)
    elif max_price:
        products = products.filter(price__lte=max_price)
        
    if min_price:
        products = products.filter(price__gte=min_price)
    
    # Sắp xếp
    selected_sort = request.GET.get('sort', '')
    if selected_sort == 'price_asc':
        products = products.order_by('price')
    elif selected_sort == 'price_desc':
        products = products.order_by('-price')
    elif selected_sort == 'rating':
        products = products.order_by('-rating')
    elif selected_sort == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('-created_at')
    
    # Phân trang
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'paginator': paginator,
        'categories': categories,
        'brands': brands,
        'scent_types': scent_types,
        'selected_categories': selected_categories,
        'selected_brands': selected_brands,
        'selected_scents': selected_scents,
        'selected_cat_ids': set(selected_categories),
        'selected_brand_names': set(selected_brands),
        'selected_scent_names': set(selected_scents),
        'selected_sort': selected_sort,
        'selected_tag': selected_tag,
        'min_price': min_price,
        'max_price': max_price,
        'price_range': price_range,
        'query': query,
        'display_tags': ["Nam", "Nữ", "Mùa Hè", "Mùa Đông", "Woody", "Floral", "Fresh", "Oriental"],
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, pk):
    """Chi tiết sản phẩm"""
    product = get_object_or_404(Product, pk=pk, is_active=True)
    reviews = product.reviews.all()
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(pk=pk)[:4]
    
    context = {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)


def category_list(request):
    """Danh sách danh mục"""
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'products/category_list.html', context)


def category_detail(request, pk):
    """Chi tiết danh mục"""
    category = get_object_or_404(Category, pk=pk)
    products = category.products.filter(is_active=True)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'products': page_obj.object_list,
    }
    return render(request, 'products/category_detail.html', context)




@login_required
def view_wishlist(request):
    """Xem danh sách yêu thích của người dùng"""
    items = WishlistItem.objects.filter(user=request.user).select_related('product')
    products = [item.product for item in items]
    context = {'items': items, 'products': products}
    return render(request, 'products/wishlist.html', context)


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, f'Đã thêm {product.name} vào danh sách yêu thích.')
    else:
        messages.info(request, f'{product.name} đã có trong danh sách yêu thích.')
    if request.is_ajax() or request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'added': created})
    return redirect('product_detail', pk=product_id)


@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    WishlistItem.objects.filter(user=request.user, product=product).delete()
    messages.success(request, f'Đã xóa {product.name} khỏi danh sách yêu thích.')
    if request.is_ajax() or request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'removed': True})
    return redirect('view_wishlist')


def subscribe_newsletter(request):
    """Đăng ký nhận bản tin"""
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        if email:
            subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
            subscriber.first_name = first_name
            subscriber.last_name = last_name
            subscriber.is_active = True
            subscriber.save()
            if created:
                messages.success(request, 'Cảm ơn bạn đã đăng ký nhận bản tin!')
            else:
                messages.info(request, 'Email này đã đăng ký nhận bản tin.')
        else:
            messages.error(request, 'Vui lòng nhập email hợp lệ.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def check_stock(request, product_id):
    """API kiểm tra tồn kho"""
    if request.is_ajax() or request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product = get_object_or_404(Product, pk=product_id)
        return JsonResponse({
            'stock': product.stock,
            'in_stock': product.stock > 0
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


def compare_products(request):
    """So sánh sản phẩm"""
    ids = request.GET.get('ids', '')
    products = []
    if ids:
        product_ids = [int(id) for id in ids.split(',') if id.isdigit()]
        products = Product.objects.filter(id__in=product_ids)
    
    context = {
        'products': products,
    }
    return render(request, 'products/compare.html', context)


def news_list(request):
    """Danh sách tin tức"""
    news_posts = NewsPost.objects.filter(is_published=True)
    paginator = Paginator(news_posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'news_posts': page_obj.object_list,
    }
    return render(request, 'products/news_list.html', context)


def news_detail(request, pk):
    """Chi tiết tin tức"""
    post = get_object_or_404(NewsPost, pk=pk, is_published=True)
    recent_posts = NewsPost.objects.filter(is_published=True).exclude(pk=pk)[:5]
    
    context = {
        'post': post,
        'recent_posts': recent_posts,
    }
    return render(request, 'products/news_detail.html', context)


def contact(request):
    """Trang liên hệ"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            messages.success(request, 'Cảm ơn bạn đã liên hệ! Chúng tôi sẽ phản hồi sớm nhất có thể.')
            return redirect('contact')
        else:
            messages.error(request, 'Vui lòng điền đầy đủ các thông tin.')
            
    return render(request, 'products/contact.html')


def about(request):
    """Trang giới thiệu"""
    return render(request, 'products/about.html')


def consultation(request):
    """Trang Di Sản & Tinh Hoa (Heritage)"""
    return render(request, 'products/consultation.html')
