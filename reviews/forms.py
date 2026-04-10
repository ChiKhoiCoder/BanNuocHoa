from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """Form đánh giá sản phẩm"""
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i}⭐') for i in range(1, 6)], attrs={'class': 'form-check-input'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tiêu đề đánh giá'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Nhận xét của bạn'}),
        }
