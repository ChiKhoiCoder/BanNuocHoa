from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    """Form tạo/chỉnh sửa sản phẩm"""
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'discount_price', 
                  'image', 'stock', 'brand', 'scent_type', 'volume', 'is_featured', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'scent_type': forms.TextInput(attrs={'class': 'form-control'}),
            'volume': forms.TextInput(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CategoryForm(forms.ModelForm):
    """Form tạo/chỉnh sửa danh mục"""
    class Meta:
        model = Category
        fields = ['name', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ProductSearchForm(forms.Form):
    """Form tìm kiếm sản phẩm"""
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tìm kiếm sản phẩm...'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Tất cả danh mục",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    min_price = forms.DecimalField(
        required=False,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Giá tối thiểu'
        })
    )
    max_price = forms.DecimalField(
        required=False,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Giá tối đa'
        })
    )
    sort = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Sắp xếp'),
            ('-created_at', 'Mới nhất'),
            ('price', 'Giá: Thấp đến Cao'),
            ('-price', 'Giá: Cao đến Thấp'),
            ('-rating', 'Đánh giá cao nhất'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
