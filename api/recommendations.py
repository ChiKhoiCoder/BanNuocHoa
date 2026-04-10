from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from products.models import Product
from api.serializers import ProductSerializer
from orders.models import OrderDetail
from django.db.models import Sum


class RecommendedProducts(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        user = request.user if request.user.is_authenticated else None
        if user:
            # Recommend based on categories from user's past orders
            categories = Product.objects.none()
            # find top categories the user purchased from
            top_cats = OrderDetail.objects.filter(order__user=user).values_list('product__category', flat=True)
            if top_cats:
                products = Product.objects.filter(category__in=top_cats, is_active=True).exclude(id__in=OrderDetail.objects.filter(order__user=user).values_list('product', flat=True))[:8]
            else:
                products = Product.objects.filter(is_active=True).order_by('-num_reviews')[:8]
        else:
            # anonymous: top selling products
            top_products = OrderDetail.objects.values('product').annotate(total_sold=Sum('quantity')).order_by('-total_sold')[:8]
            product_ids = [p['product'] for p in top_products]
            products = Product.objects.filter(id__in=product_ids, is_active=True)

        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
