from django import forms
from .models import Review
from apps.rooms.models import Room


class ReviewForm(forms.ModelForm):
    room = forms.ModelChoiceField(
        queryset=Room.objects.filter(is_active=True),
        label="Номер",
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = Review
        fields = ['room', 'text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Поделитесь впечатлениями об отдыхе...',
            }),
            'rating': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'room': 'Какой номер вы бронировали?',
            'text': 'Ваш отзыв',
            'rating': 'Оценка',
        }