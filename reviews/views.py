from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Review
from .forms import ReviewForm
from products.models import Product
from orders.models import Order, OrderDetail


@login_required(login_url='login')
def add_review(request, product_id):
    """Thêm đánh giá sản phẩm"""
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    
    # Kiểm tra xem người dùng đã mua sản phẩm này chưa
    has_purchased = OrderDetail.objects.filter(
        order__user=request.user,
        product=product,
        order__status__in=['completed', 'shipped']
    ).exists()
    
    try:
        review = Review.objects.get(product=product, user=request.user)
        is_update = True
    except Review.DoesNotExist:
        review = None
        is_update = False
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            
            # Cập nhật rating của sản phẩm
            reviews = product.reviews.all()
            avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews.exists() else 0
            product.rating = round(avg_rating, 2)
            product.num_reviews = reviews.count()
            product.save()
            
            if is_update:
                messages.success(request, 'Cập nhật đánh giá thành công!')
            else:
                messages.success(request, 'Thêm đánh giá thành công!')
            return redirect('product_detail', pk=product_id)
    else:
        form = ReviewForm(instance=review)
    
    context = {
        'form': form,
        'product': product,
        'is_update': is_update,
        'has_purchased': has_purchased,
    }
    return render(request, 'reviews/review_form.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def delete_review(request, review_id):
    """Xóa đánh giá"""
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    product = review.product
    review.delete()
    
    # Cập nhật rating của sản phẩm
    reviews = product.reviews.all()
    avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews.exists() else 0
    product.rating = round(avg_rating, 2)
    product.num_reviews = reviews.count()
    product.save()
    
    messages.success(request, 'Xóa đánh giá thành công!')
    return redirect('product_detail', pk=product.id)
