from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """Форма добавления отзыва."""
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Поделитесь впечатлениями об отдыхе...',
            }),
            'rating': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'text': 'Ваш отзыв',
            'rating': 'Оценка',
        }