from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from .models import Product


@require_http_methods(["GET"])
def live_search(request):
    """
    Live search endpoint - returns product suggestions as user types
    """
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({
            'success': False,
            'message': 'Query too short'
        })
    
    # Search in name, brand, description
    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(brand__icontains=query) |
        Q(description__icontains=query),
        is_active=True
    )[:10]  # Limit to 10 results
    
    results = []
    for product in products:
        results.append({
            'id': product.id,
            'name': product.name,
            'brand': product.brand,
            'price': float(product.get_price()),
            'image': product.image.url if product.image else '',
            'url': f'/products/{product.id}/',
            'rating': float(product.rating) if product.rating else 0,
            'in_stock': product.stock > 0,
        })
    
    return JsonResponse({
        'success': True,
        'results': results,
        'count': len(results)
    })


@require_http_methods(["GET"])
def filter_products(request):
    """
    Advanced product filtering endpoint
    Supports: category, price range, brand, scent_type, tags, sort
    """
    # Get filter parameters
    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    brands = request.GET.getlist('brand')
    scent_types = request.GET.getlist('scent_type')
    tags = request.GET.getlist('tag')
    sort_by = request.GET.get('sort', 'name')
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 12))
    
    # Start with active products
    products = Product.objects.filter(is_active=True)
    
    # Apply filters
    if category_id:
        products = products.filter(category_id=category_id)
    
    if min_price:
        products = products.filter(price__gte=float(min_price))
    
    if max_price:
        products = products.filter(price__lte=float(max_price))
    
    if brands:
        products = products.filter(brand__in=brands)
    
    if scent_types:
        products = products.filter(scent_type__in=scent_types)
    
    if tags:
        # Tag filtering (assuming tags are in description or a separate field)
        tag_query = Q()
        for tag in tags:
            tag_query |= Q(description__icontains=tag)
        products = products.filter(tag_query)
    
    # Sorting
    sort_options = {
        'name': 'name',
        'price_asc': 'price',
        'price_desc': '-price',
        'rating': '-rating',
        'newest': '-created_at',
    }
    products = products.order_by(sort_options.get(sort_by, 'name'))
    
    # Pagination
    total_count = products.count()
    start = (page - 1) * per_page
    end = start + per_page
    products_page = products[start:end]
    
    # Build response
    results = []
    for product in products_page:
        results.append({
            'id': product.id,
            'name': product.name,
            'brand': product.brand,
            'price': float(product.price),
            'discount_price': float(product.discount_price) if product.discount_price else None,
            'display_price': float(product.get_price()),
            'image': product.image.url if product.image else '',
            'url': f'/products/{product.id}/',
            'rating': float(product.rating) if product.rating else 0,
            'num_reviews': product.num_reviews,
            'in_stock': product.stock > 0,
            'is_featured': product.is_featured,
        })
    
    return JsonResponse({
        'success': True,
        'results': results,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total_count': total_count,
            'total_pages': (total_count + per_page - 1) // per_page,
            'has_next': end < total_count,
            'has_prev': page > 1,
        }
    })


@require_http_methods(["GET"])
def get_filter_options(request):
    """
    Get available filter options (brands, scent types, price range)
    """
    category_id = request.GET.get('category')
    
    products = Product.objects.filter(is_active=True)
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Get unique brands
    brands = products.values_list('brand', flat=True).distinct().order_by('brand')
    
    # Get unique scent types
    scent_types = products.values_list('scent_type', flat=True).distinct().order_by('scent_type')
    scent_types = [st for st in scent_types if st]  # Remove None values
    
    # Get price range
    prices = products.values_list('price', flat=True)
    min_price = min(prices) if prices else 0
    max_price = max(prices) if prices else 0
    
    return JsonResponse({
        'success': True,
        'brands': list(brands),
        'scent_types': list(scent_types),
        'price_range': {
            'min': float(min_price),
            'max': float(max_price),
        }
    })
